# -*- coding: utf-8 -*-
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin,AnonymousUserMixin
from markdown import markdown
import bleach
from . import db
from . import login_manager

class Permission:
    FOLLOW = 0x01
    COMMENT = 0x02
    WRITE_ARTICLES = 0x04
    MODERATE_COMMENTS = 0x08
    ADMINISTER = 0x80

class Role(db.Model,UserMixin):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key =True)
    name = db.Column(db.Unicode(128),unique=True)
    default = db.Column(db.Boolean, default=True, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __init__(self, name):
        self.name = name

    @staticmethod
    def insert_roles():
        roles = {
                'User'          : (Permission.FOLLOW|
                                   Permission.COMMENT|
                                   Permission.WRITE_ARTICLES,
                                   True),
                'Moderator'     : (Permission.FOLLOW|
                                   Permission.COMMENT|
                                   Permission.WRITE_ARTICLES|
                                   Permission.MODERATE_COMMENTS,
                                   False),
                'Administrator' : (0xFF,
                                   False),
                }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
            db.session.commit()

    def __repr__(self):
        return '<Role %r>' % self.name

class User(db.Model,UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Unicode(128), unique=True)
    email = db.Column(db.Unicode(128), unique=True)
    password_hash = db.Column(db.Unicode(128))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password
        if self.role is None:
            self.role = Role.query.filter_by(default=True).first()

    def __repr__(self):
        return '<User %r>' % self.username

    @property
    def password(self):
        raise AttributeError('password is not a readable attribure')

    @password.setter
    def password(self,password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)

    def can(self,permissions):
        return self.role is not None and\
                (self.role.permissions & permissions) == permissions

    def is_administrator(self):
        return self.can(Permission.ADMINISTER)

class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False
    def is_administrator(self):
        return False

login_manager.anonymous_user = AnonymousUser

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    body = db.Column(db.Text)
    body_html = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code', 'div',
                        'em', 'i', 'img', 'li', 'ol', 'pre', 'strong', 'ul',
                        'h1', 'h2', 'h3', 'p', 'src']
        allowed_attrs = {
        '*': ['class', 'align'],
        'a': ['href', 'rel'],
        'img': ['src','alt', 'width', 'height'],
        }
        target.body_html = bleach.linkify(bleach.clean(
                                        markdown(value, output_format='html'),
                                        tags=allowed_tags,
                                        attributes=allowed_attrs,
                                        strip=True))

db.event.listen(Post.body, 'set', Post.on_changed_body)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
