# -*- coding: utf-8 -*-
from . import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(128), unique=True)
    email = db.Column(db.Unicode(128), unique=True)
    password_hash = db.Column(db.Unicode(128))
    def __init__(self, name, email):
        self.name = name
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.name
