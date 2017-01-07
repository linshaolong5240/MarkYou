# -*- coding: utf-8 -*-

from config import load_config
from flask import Flask
from flask import request
from flask import render_template
from flask_bootstrap import Bootstrap
from flask_wtf import Form
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
config = load_config()
app.config.from_object(config)
db = SQLAlchemy(app)
bootstrap = Bootstrap(app)

@app.route('/')
def index():
    user_agent = request.headers.get('user-agent')
    return render_template('index.html',user_agent=user_agent)

@app.route('/user/<name>')
def user(name):
    return render_template('user.html',user_name=name)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup')
def sign_up():
    return render_template('sign_up.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

if __name__ == "__main__":
    app.run()
