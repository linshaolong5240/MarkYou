# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from flask_pagedown.fields import PageDownField
from wtforms import TextAreaField,StringField,PasswordField,BooleanField,SubmitField
from wtforms.validators import Required

class FormLogin(FlaskForm):
    username    = StringField('Username', validators = [Required()])
    password    = PasswordField('Password', validators = [Required()])
    remember_me = BooleanField('Remember me')
    submit      = SubmitField('Submit')

class FormPost(FlaskForm):
    title    = StringField('Title', validators = [Required()])
    pagedown = PageDownField("What's on your mind?", validators = [Required()])
    submit   = SubmitField('Submit')
