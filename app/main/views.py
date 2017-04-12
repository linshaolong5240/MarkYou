# -*- coding: utf-8 -*-
from flask import current_app,request,render_template,redirect,url_for,flash
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
        return redirect(url_for('blueprint_main.index'))
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(page, per_page=current_app.config['POSTS_PER_PAGE'], error_out=False)
    posts = pagination.items
    user_agent = request.headers.get('user-agent')
    return render_template('index.html',form=form, posts=posts, pagination=pagination, user_agent=user_agent)

@blueprint_main.route('/user/<username>')
def user(username):
    user_agent = request.headers.get('user-agent')
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template('user.html',user_agent=user_agent,user=user, posts=posts)

@blueprint_main.route('/login',methods = ['GET','POST'])
def login():
    user_agent = request.headers.get('user-agent')
    form = FormLogin()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(form.password.data) :
            flash('login')
            login_user(user,form.remeber_me.data)
            return redirect(url_for('blueprint_main.index'))
        else:
            flash('login error')
    return render_template('login.html', form=form, user_agent=user_agent)

@blueprint_main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('logout')
    return redirect(url_for('blueprint_main.index'))

