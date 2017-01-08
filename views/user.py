# -*- coding: utf-8 -*-
from flask import Blueprint
from flask import request
from flask import render_template

blueprint = Blueprint('user',__name__)

@blueprint.route('/login')
def login():
    user_agent = request.headers.get('user-agent')
    return render_template('login.html',user_agent=user_agent)
