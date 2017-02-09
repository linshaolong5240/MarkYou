# -*- coding: utf-8 -*-
from flask import Blueprint
from flask import request
from flask import render_template
from flask import redirect
from flask import url_for
from flask import flash
from forms.form_login import FormLogin

blueprint = Blueprint('user',__name__)

@blueprint.route('/login',methods = ['GET','POST'])
def login():
    user_agent = request.headers.get('user-agent')
    form = FormLogin()
    if form.validate_on_submit():
        user_name = form.user_name
        flash('user logined')
        return redirect(url_for('home.index'));
    return render_template('login.html', form=form, user_agent=user_agent)
