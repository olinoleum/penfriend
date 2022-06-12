# Standard library imports
import datetime as dt
import os.path
import enum

# Third party imports
import flask_login
from flask import current_app
from flask_login import UserMixin
from sqlalchemy import event
from sqlalchemy.sql import func
#from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from fuzzywuzzy import fuzz

# Local application imports
from penfriend import db, login


@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    receiver = db.Column(db.Integer(), db.ForeignKey('user.id'))
    ts = db.Column(db.DateTime(timezone=True), server_default=func.now())
    msg = db.Column(db.String)
    lang = db.Column(db.String)
    translated_msg = db.Column(db.String)
    translated_lang = db.Column(db.String)
    corrected_msg = db.Column(db.String)

    def __repr__(self):
        return f"{self.id} - {self.user_id} - {self.msg}"

    @property
    def is_ai(self) -> bool:
        return True if self.user_id == 1 else False

    @property
    def is_corrected(self) -> bool:
        if self.corrected_msg is None:
            return False

        if fuzz.ratio(self.msg, self.corrected_msg) < 95:
            return True
        else:
            return False


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String(88))
    cookie_id = db.Column(db.Integer)
    messages = db.relationship("Message", backref="message", primaryjoin=id==Message.user_id, lazy='dynamic')

    def __repr__(self):
        return f"{self.id} - {self.email} - {self.cookie_id}"


@event.listens_for(User.__table__, "after_create")
def create_bot_user(*args, **kwargs):
    bot_user = User(email="bot@bot.com")

    db.session.add(bot_user)
    db.session.commit()
