# -*- coding: utf-8 -*-
from flask import Blueprint
from flask import request
from flask import render_template
from forms.form_login import FormLogin

blueprint = Blueprint('user',__name__)

@blueprint.route('/login',methods = ['GET','POST'])
def login():
    user_agent = request.headers.get('user-agent')
    form = FormLogin()
    return render_template('login.html', form=form, user_agent=user_agent)
