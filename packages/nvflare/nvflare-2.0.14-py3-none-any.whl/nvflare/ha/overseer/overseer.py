from datetime import datetime
from flask import request, jsonify

from nvflare.ha.overseer.app import app

from nvflare.ha.overseer.utils import (
    simple_PSP_policy,
    promote_sp,
    update_sp_state,
    get_primary_sp,
    get_all_sp,
    do_refresh,
)


@app.route("/api/v1/heartbeat", methods=["GET", "POST"])
def heartbeat():
    if request.method == "POST":
        req = request.json
        project = req.get("project")
        role = req.get("role")
        if project is None or role is None:
            return jsonify({"error": "project and role must be provided"})
        now = datetime.utcnow()
        update_sp_state(project, now)
        if role == "server":
            sp_end_point = req.get("sp_end_point")
            if sp_end_point is None:
                return jsonify({"error": "sp_end_point is not provided"})
            incoming_sp = dict(sp_end_point=sp_end_point, project=project)
            psp = simple_PSP_policy(incoming_sp, now)
        elif role in ["client", "admin"]:
            psp = get_primary_sp(project)
        else:
            psp = {}
        return jsonify({"primary_sp": psp, "sp_list": get_all_sp(project)})


@app.route("/api/v1/promote", methods=["GET", "POST"])
def promote():
    if request.method == "POST":
        req = request.json
        sp_end_point = req.get("sp_end_point", "")
        project = req.get("project", "")
        if project and sp_end_point:
            incoming_sp = dict(sp_end_point=sp_end_point, project=project)
            err, result = promote_sp(incoming_sp)
            if not err:
                return jsonify({"primary_sp": result})
            else:
                return jsonify({"Error": result})
        else:
            return jsonify({"Error": "Wrong project or sp_end_point."})


@app.route("/api/v1/refresh")
def refresh():
    do_refresh()
    return jsonify({"Status": "Success"})


if __name__ == "__main__":
    app.run()
