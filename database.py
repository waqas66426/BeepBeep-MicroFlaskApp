# encoding: utf8
from werkzeug.security import generate_password_hash, check_password_hash
import enum
from sqlalchemy.orm import relationship, backref
from flask_sqlalchemy import SQLAlchemy
from decimal import Decimal

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.Unicode(128), nullable=False)
    firstname = db.Column(db.Unicode(128))
    lastname = db.Column(db.Unicode(128))
    password = db.Column(db.Unicode(128))
    strava_token = db.Column(db.String(128))
    age = db.Column(db.Integer)
    weight = db.Column(db.Numeric(4, 1))
    max_hr = db.Column(db.Integer)
    rest_hr = db.Column(db.Integer)
    vo2max = db.Column(db.Numeric(4, 2))
    is_active = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False)
    is_anonymous = False

    def __init__(self, *args, **kw):
        super(User, self).__init__(*args, **kw)
        self._authenticated = False

    def set_password(self, password):
        self.password = generate_password_hash(password)

    @property
    def is_authenticated(self):
        return self._authenticated

    def authenticate(self, password):
        #checked = self.password == password
        checked = check_password_hash(self.password, password)
        self._authenticated = checked
        return self._authenticated

    def to_json(self, secure=False):
        res = {}
        for attr in ('id', 'email', 'firstname', 'lastname', 'age', 'weight', 'max_hr', 'rest_hr', 'vo2max', 'password'):
            value = getattr(self, attr)
            if isinstance(value, Decimal):
                value = float(value)
            res[attr] = (value if value is not None else "")
        if secure:
            res['strava_token'] = self.strava_token
        return res

    def get_id(self):
        return self.id


def _delete_user(user):
    # delete cascade
    db.session.delete(user)
    db.session.commit()
