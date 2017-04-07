# -*- coding: utf-8 -*-
from flask import request
from flask import render_template
from flask import redirect
from flask import url_for
from flask import flash
from flask_login import login_user,logout_user,login_required
from .forms import FormLogin
from . import blueprint_main
from ..models import User

@blueprint_main.route('/')
def index():
    user_agent = request.headers.get('user-agent')
    return render_template('index.html',user_agent=user_agent)

@blueprint_main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first()
    user_agent = request.headers.get('user-agent')
    return render_template('user.html',user_agent=user_agent,user=user)

@blueprint_main.route('/login',methods = ['GET','POST'])
def login():
    user_agent = request.headers.get('user-agent')
    form = FormLogin()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(form.password.data) :
            flash('login')
            login_user(user,form.remeber_me.data)
            return redirect(url_for('main.index'))
        else:
            flash('login error')
    return render_template('login.html', form=form, user_agent=user_agent)

@blueprint_main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('logout')
    return redirect(url_for('main.index'))
