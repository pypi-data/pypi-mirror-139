import os
from flask_sqlalchemy import SQLAlchemy

from .app import app

app.config.from_mapping(
    SECRET_KEY=os.environ.get("SECRET_KEY") or "dev_key",
    SQLALCHEMY_DATABASE_URI=os.environ.get("DATABASE_URL") or "sqlite:///" + os.path.join(os.getcwd(), "status.sqlite"),
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
)
db = SQLAlchemy(app)


class SP(db.Model):
    sp_end_point = db.Column(db.String(80), primary_key=True)
    project = db.Column(db.String(20), primary_key=True)
    state = db.Column(db.String(10), nullable=False)
    last_heartbeat = db.Column(db.String(40))
    primary = db.Column(db.Boolean(), default=False)
    service_session_id = db.Column(db.String(40))

    def asdict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __repr__(self):
        return str(self.asdict())


def _dict_or_empty(sp):
    return sp.asdict() if sp else {}


def do_refresh():
    db.drop_all()
    db.create_all()


def get_all_sp(project):
    all_sp = SP.query.filter_by(project=project)
    return [_dict_or_empty(sp) for sp in all_sp]


def get_primary_sp(project):
    sp = SP.query.filter_by(project=project, primary=True).first()
    return _dict_or_empty(sp)


def update_sp(sp):
    predicate = {k: sp[k] for k in ["sp_end_point", "project"]}
    existing_sp = SP.query.filter_by(**predicate).first()
    if existing_sp:
        existing_sp.last_heartbeat = sp["last_heartbeat"]
        existing_sp.service_session_id = sp.get("service_session_id", "")
        existing_sp.primary = sp.get("primary", False)
        existing_sp.state = sp.get("state")
        db.session.add(existing_sp)
    else:
        sp = SP(**sp)
        db.session.add(sp)
    db.session.commit()


def get_sp_by(predicate: dict):
    sp = SP.query.filter_by(**predicate).first()
    return _dict_or_empty(sp)
