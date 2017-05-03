# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from flask_pagedown.fields import PageDownField
from wtforms import TextAreaField,StringField,PasswordField,BooleanField,SubmitField
from wtforms.validators import Required

class FormLogin(FlaskForm):
    username   = StringField('username', validators   = [Required()])
    password   = PasswordField('password', validators = [Required()])
    remeber_me = BooleanField('remeber me')
    submit     = SubmitField('Submit')

class FormPost(FlaskForm):
    body   = PageDownField("what's on your mind?", validators = [Required()])
    submit = SubmitField('Submit')
