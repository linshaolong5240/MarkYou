from flask_wtf import Form
from wtforms import StringField, SubmitField 
from wtforms.validators import Required

class FormLogin(Form):
    user_name = StringField('user name', validators=[Required()])
    password = StringField('password', validators=[Required()])
    submit = SubmitField('Submit')
