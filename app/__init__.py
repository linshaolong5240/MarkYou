# -*- coding: utf-8 -*-
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_pagedown import PageDown
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail,Message

db = SQLAlchemy()
bootstrap = Bootstrap()
moment = Moment()
pagedown = PageDown()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'blueprint_main.login'
mail = Mail()

def create_app(configname_name):
    app = Flask(__name__)
    from config import config
    app.config.from_object(config[configname_name])
    from .main import blueprint_main
    app.register_blueprint(blueprint_main, url_prefix='')

    db.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)
    pagedown.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    return app
