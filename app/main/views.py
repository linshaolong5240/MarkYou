# -*- coding: utf-8 -*-
from flask import request
from flask import render_template
from flask import redirect
from flask import url_for
from flask import flash
from flask_login import login_user,logout_user,login_required,current_user
from .forms import FormLogin,FormPost
from . import blueprint_main
from .. import db
from ..models import User,Role,Post,Permission

@blueprint_main.route('/', methods=['GET', 'POST'])
def index():
    form = FormPost()
    if current_user.can(Permission.WRITE_ARTICLES) and\
            form.validate_on_submit():
        post = Post(body=form.body.data, author=current_user._get_current_object())
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('main.index'))
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    user_agent = request.headers.get('user-agent')
    return render_template('index.html',form=form, posts=posts, user_agent=user_agent)

@blueprint_main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first()
    user_agent = request.headers.get('user-agent')
    return render_template('user.html',user_agent=user_agent,user=user)

@blueprint_main.route('/login',methods = ['GET','POST'])
def login():
    user_agent = request.headers.get('user-agent')
    form = FormLogin()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(form.password.data) :
            flash('login')
            login_user(user,form.remeber_me.data)
            return redirect(url_for('main.index'))
        else:
            flash('login error')
    return render_template('login.html', form=form, user_agent=user_agent)

@blueprint_main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('logout')
    return redirect(url_for('main.index'))
