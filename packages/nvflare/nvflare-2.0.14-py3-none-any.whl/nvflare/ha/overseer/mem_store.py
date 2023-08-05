import threading

data_store = dict()
data_store["SP"] = dict()
data_store_lock = threading.Lock()


def do_refresh():
    with data_store_lock:
        data_store = dict()


def _primary_key(sp):
    return f'{sp["project"]}/{sp["sp_end_point"]}'


def get_all_sp(project):
    with data_store_lock:
        sp_list = [v for v in data_store["SP"].values() if v["project"] == project]
    return sp_list


def get_primary_sp(project):
    psp = {}
    with data_store_lock:
        for _, sp in data_store["SP"].items():
            if sp["primary"] == True and sp["project"] == project:
                psp = sp
                break
    return psp


def update_sp(sp):
    with data_store_lock:
        key = _primary_key(sp)
        existing_sp = data_store["SP"].get(key)
        if existing_sp:
            existing_sp.update(sp)
            data_store["SP"][key] = existing_sp
        else:
            data_store["SP"][key] = sp


def get_sp_by(predicate: dict):
    result = {}
    with data_store_lock:
        for sp in data_store["SP"].values():
            if all(sp[k] == predicate[k] for k in predicate):
                result = sp
                break
    return result
