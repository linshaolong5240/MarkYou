# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from flask_pagedown.fields import PageDownField
from wtforms import TextAreaField,StringField,PasswordField,BooleanField,SubmitField
from wtforms.validators import Required

class FormLogin(FlaskForm):
    username   = StringField('Username', validators=[Required()])
    password   = PasswordField('Password', validators = [Required()])
    remeber_me = BooleanField('Remeber me')
    submit     = SubmitField('Submit')

class FormPost(FlaskForm):
    pagedown   = PageDownField("what's on your mind?", validators = [Required()])
    submit = SubmitField('Submit')
