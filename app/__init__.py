# -*- coding: utf-8 -*-
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
bootstrap = Bootstrap()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'main.login'

def create_app(configname_name):
    app = Flask(__name__)
    from config import config
    app.config.from_object(config[configname_name])
    from .main import blueprint_main
    app.register_blueprint(blueprint_main, url_prefix='')

    db.init_app(app)
    bootstrap.init_app(app)
    login_manager.init_app(app)
    print('create app')
    return app
