# -*- coding: utf-8 -*-
import os
import hashlib
from werkzeug.utils import secure_filename
from flask import current_app,request,render_template,redirect,url_for,flash,abort
from flask import Response
from flask_login import login_user,logout_user,login_required,current_user
from .forms import FormLogin,FormPost,FormFile
from . import blueprint_main
from .. import db
from ..models import User,Role,Post,Permission

@blueprint_main.route('/')
def index():
    # if current_user.can(Permission.WRITE_ARTICLES) and\
    #         form.validate_on_submit():
    #     post = Post(body=form.pagedown.data, author=current_user._get_current_object())
    #     db.session.add(post)
    #     db.session.commit()
    #     return redirect(url_for('blueprint_main.index'))
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(page, per_page=current_app.config['POSTS_PER_PAGE'], error_out=False)
    posts = pagination.items
    user_agent = request.headers.get('user-agent')
    return render_template('index.html', posts=posts, pagination=pagination, user_agent=user_agent)


@blueprint_main.route('/file/')
@blueprint_main.route('/file/<filename>')
def file(filename=None):
    def get_mimetype(filename):
        mimetype = 'application/octet-stream'
        if '.' in filename:
            extension = filename.rsplit('.', 1)[1]
            if extension.find('jp') != -1:#if not found return -1
               mimetype = 'image/jpeg'
        return mimetype

    if filename:
        filename = secure_filename(filename)
        try:
            with open(os.path.join(current_app.config['UPLOAD_FOLDER'], filename[:2], filename), 'rb') as file:
                return Response(file.read(), mimetype=get_mimetype(filename))
        except Exception as error:
                return render_template('error.html',error=error)
    else:
        filename_list = []
        for a in os.walk(current_app.config['UPLOAD_FOLDER']):#(root,dirs,files)
            if a[2]:
                filename_list.append(a[2][0])
        return render_template('file.html', filename_list=filename_list)

@blueprint_main.route('/upload_file', methods=['GET', 'POST'])
def upload_file():
    def allowed_file(filename):
        return '.' in filename and \
        filename.rsplit('.', 1)[1] in current_app.config['ALLOWED_EXTENSIONS']
    user_agent = request.headers.get('user-agent')
    form = FormFile()
    if form.validate_on_submit():
        temp_file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'tempfile')
        file = form.file.data
        if allowed_file(file.filename):
            # file_name = secure_filename(file.filename)
            sha1 = hashlib.sha1(file.stream.read())
            file_name = sha1.hexdigest() + '.' + file.filename.rsplit('.', 1)[1]
            file_save_path = os.path.join(current_app.config['UPLOAD_FOLDER'] , file_name[:2])
            if os.path.isdir(file_save_path) == False:
                os.mkdir(file_save_path)
            file.stream.seek(0)
            file.save(os.path.join(file_save_path,file_name))


    return render_template('upload_file.html', form=form, user_agent=user_agent)

@blueprint_main.route('/file_delete/<filename>')
def file_delete(filename):
    try:
        os.remove(os.path.join(current_app.config['UPLOAD_FOLDER'],filename[:2],filename))
    except Exception as error:
            return render_template('error.html',error=error)
    return redirect(url_for('blueprint_main.file'))

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
            login_user(user,form.remember_me.data)
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

@blueprint_main.route('/post/<int:id>')
def post(id):
    post = Post.query.get_or_404(id)
    return render_template('post.html', posts=[post])

@blueprint_main.route('/write_post', methods = ['GET','POST'])
def write_post():
    if current_user.can(Permission.WRITE_ARTICLES) == False:
        abort(404)

    form = FormPost()
    if form.validate_on_submit():
        post = Post(title=form.title.data, body=form.pagedown.data, author=current_user._get_current_object())
        db.session.add(post)
        db.session.commit()
        flash("The post has been commited.")
        return redirect(url_for('blueprint_main.index'))
    return render_template("edit_post.html", form=form)

@blueprint_main.route('/edit_post/<int:id>', methods = ['GET','POST'])
def edit_post(id):
    post = Post.query.get_or_404(id)
    if current_user != post.author and not current_user.is_administrator():
        abort(404)

    form = FormPost()
    if form.validate_on_submit():
        post.title = form.title.data
        post.body = form.pagedown.data
        db.session.add(post)
        db.session.commit()
        flash("The post has been updated.")
        return redirect(url_for('blueprint_main.post', id=post.id))
    form.title.data = post.title
    form.pagedown.data = post.body
    return render_template("edit_post.html", form=form)

@blueprint_main.route('/delete_post/<int:id>', methods = ['GET','POST'])
def delete_post(id):
    post = Post.query.get_or_404(id)
    if current_user != post.author and not current_user.is_administrator():
        abort(404)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('blueprint_main.index'))
