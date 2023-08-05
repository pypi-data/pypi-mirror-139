import argparse

import threading
import time
from typing import Any, Dict, Optional

from requests import Request, Session, codes
from pprint import pprint

from nvflare.apis.overseer_spec import OverseerAgent, SP


class HttpOverseerAgent(OverseerAgent):
    def __init__(self):
        self._session = None
        self._overseer_end_point = None
        self._role = None
        self._status_lock = threading.Lock()
        self._report_and_query = threading.Thread(target=self._rnq_worker, args=())
        self._psp = SP()
        self._flag = threading.Event()
        self._ca_path = None
        self._cert_path = None
        self._prv_key_path = None
        self._last_service_session_id = ""
        self._asked_to_exit = False

    def _send(
        self, api_point, headers: Optional[Dict[str, Any]] = None, payload: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        req = Request("POST", api_point, json=payload, headers=headers)
        prepared = self._session.prepare_request(req)
        resp = self._session.send(prepared)
        return resp

    def set_secure_context(self, ca_path: str, cert_path: str = "", prv_key_path: str = ""):
        self._ca_path = ca_path
        self._cert_path = cert_path
        self._prv_key_path = prv_key_path

    def initialize(
        self,
        overseer_end_point: str,
        project: str,
        role: str,
        name: str,
        fl_port: str = "",
        adm_port: str = "",
        aux: dict = {},
        *args,
        **kwargs,
    ):
        self._session = Session()
        self._overseer_end_point = overseer_end_point
        self._role = role
        self._project = project
        if self._ca_path:
            self._session.verify = self._ca_path
        self._aux = aux
        if self._role == "server":
            self._sp_end_point = ":".join([name, fl_port, adm_port])
        self._args = args
        self._kwargs = kwargs
        self._sleep = self._kwargs.get("sleep", 1)

    def start(self, update_callback=None):
        if update_callback:
            self._update_callback = update_callback
        if self._role != "admin":
            self._report_and_query.start()
            self._flag.set()

    def pause(self):
        self._flag.clear()

    def resume(self):
        self._flag.set()

    def end(self):
        if self._role != "admin":
            self._flag.set()
            self._asked_to_exit = True
            self._report_and_query.join()

    def get_primary_sp(self) -> SP:
        """Return current primary service provider.

        If primary sp not available, such as not reported by SD, connection to SD not established yet
        the name and ports will be empty strings.
        """
        return self._psp

    def one_report_and_query(self):
        data = self._prepare_data()
        api_point = self._overseer_end_point + "/heartbeat"
        self._rnq(api_point, headers=None, data=data)

    def promote_sp(self, sp_end_point):
        api_point = self._overseer_end_point + "/promote"
        return self._send(api_point, headers=None, payload={"sp_end_point": sp_end_point, "project": self._project})

    def _handle_ssid(self, ssid):
        if self._last_service_session_id != ssid:
            self._last_service_session_id = ssid
            if self._update_callback:
                self._update_callback(self)

    def _prepare_data(self):
        data = dict(role=self._role, project=self._project)
        data.update(self._aux)
        return data

    def _rnq_worker(self):
        data = self._prepare_data()
        if self._role == "server":
            data["sp_end_point"] = self._sp_end_point
        api_point = self._overseer_end_point + "/heartbeat"
        while not self._asked_to_exit:
            self._flag.wait()
            self._rnq(api_point, headers=None, data=data)
            time.sleep(self._sleep)

    def _rnq(self, api_point, headers, data):
        resp = self._send(api_point, headers=headers, payload=data)
        if resp.status_code != codes.ok:
            return
        self._overseer_info = resp.json()
        psp = self._overseer_info.get("primary_sp")
        if psp:
            name, fl_port, adm_port = psp.get("sp_end_point").split(":")
            service_session_id = psp.get("service_session_id", "")
            self._psp = SP(name, fl_port, adm_port, service_session_id, True)
            # last_heartbeat = psp.get("last_heartbeat", "")
            self._handle_ssid(service_session_id)
        else:
            self._psp = SP()
            service_session_id = ""
            self._handle_ssid(service_session_id)


def simple_callback(overseer_agent):
    print(f"\nGot callback {overseer_agent.get_primary_sp()}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--project", type=str, default="example_project", help="project name")
    parser.add_argument("-r", "--role", type=str, help="role (server, client or admin)")
    parser.add_argument("-n", "--name", type=str, help="globally unique name")
    parser.add_argument("-f", "--fl_port", type=str, help="fl port number")
    parser.add_argument("-a", "--adm_port", type=str, help="adm port number")
    parser.add_argument("-s", "--sleep", type=float, help="sleep (seconds) in heartbeat")
    parser.add_argument("-c", "--ca_path", type=str, help="root CA path")
    parser.add_argument("-o", "--overseer_url", type=str, help="Overseer URL")

    args = parser.parse_args()

    overseer_agent = HttpOverseerAgent()

    if args.ca_path:
        overseer_agent.set_secure_context(ca_path=args.ca_path)
    overseer_agent.initialize(
        overseer_end_point=args.overseer_url,
        project=args.project,
        role=args.role,
        name=args.name,
        fl_port=args.fl_port,
        adm_port=args.adm_port,
        sleep=args.sleep,
    )
    overseer_agent.start(simple_callback)
    while True:
        answer = input("(p)ause/(r)esume/(s)witch/(d)ump/(e)nd? ")
        normalized_answer = answer.strip().upper()
        if normalized_answer == "P":
            overseer_agent.pause()
        elif normalized_answer == "R":
            overseer_agent.resume()
        elif normalized_answer == "E":
            overseer_agent.end()
            break
        elif normalized_answer == "S":
            resp = overseer_agent.promote_sp("localhost:1001:1002")
            pprint(resp.json())
        elif normalized_answer == "D":
            pprint(overseer_agent._overseer_info)


if __name__ == "__main__":
    main()
