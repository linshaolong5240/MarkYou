# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Required

class FormLogin(FlaskForm):
    user_name = StringField('user name', validators=[Required()])
    password = StringField('password', validators=[Required()])
    submit = SubmitField('Submit')
