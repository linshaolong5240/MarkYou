# -*- coding: utf-8 -*-
from flask import request
from flask import render_template
from flask import redirect
from flask import url_for
from flask import flash
from .forms import FormLogin
from . import blueprint_main
from ..models import User

@blueprint_main.route('/')
def index():
    user_agent = request.headers.get('user-agent')
    return render_template('index.html',user_agent=user_agent)


@blueprint_main.route('/sign_in',methods = ['GET','POST'])
def sign_in():
    user_agent = request.headers.get('user-agent')
    form = FormLogin()
    if form.validate_on_submit():
        user = User.query.filter_by(name=form.user_name.data).first()
        if user is not None and user.verify_password(form.password.data) :
            flash('user sign in')
            return redirect(url_for('main.index'))
        else:
            flash('sign in error')
    return render_template('sign_in.html', form=form, user_agent=user_agent)

