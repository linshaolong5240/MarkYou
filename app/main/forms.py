# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Required

class FormLogin(FlaskForm):
    username = StringField('username', validators=[Required()])
    password = StringField('password', validators=[Required()])
    submit = SubmitField('Submit')
