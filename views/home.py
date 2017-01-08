# -*- coding: utf-8 -*-
from flask import Blueprint
from flask import request
from flask import render_template

blueprint = Blueprint('home',__name__)

@blueprint.route('/')
def index():
    user_agent = request.headers.get('user-agent')
    return render_template('index.html',user_agent=user_agent)
