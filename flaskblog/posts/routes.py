import base64
import os
from flask import (app, render_template, url_for, flash, redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from flaskblog import db
from flaskblog.models import Post
from flaskblog.posts.forms import NewBlogForm, UpdateBlogForm
from flaskblog.posts.utils import save_blog_image
from werkzeug.utils import secure_filename

posts = Blueprint('posts', __name__)

@posts.route("/new/blogpost",methods=('GET', 'POST'))
@login_required
def new_blog_post():
    form = NewBlogForm()

    if form.blog_image.data:
        file = request.files[form.blog_image.name]
        filename = secure_filename(file.filename)
        file_path = str('/static/blog_images/'+filename)
        file.save(os.path.join('flaskblog\\static\\blog_images', filename))

    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user, blog_image=file_path)
        db.session.add(post)
        db.session.commit()
        flash(f'Your blog has been posted successfully!', 'success')
        return redirect(url_for('main.home'))
        
    return render_template('new_blog_post.html', title='New Post', form=form)




@posts.route("/viewblog/<int:post_id>",methods=('GET', 'POST'))
def view_blog(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('view_blog.html', title=post.title, post=post)



@posts.route("/viewblog/update/<int:post_id>",methods=['GET', 'POST'])
@login_required
def update_blog(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = UpdateBlogForm()

    if form.blog_image.data:
        file = request.files[form.blog_image.name]
        filename = secure_filename(file.filename)
        file_path = str('/static/blog_images/'+filename)
        file.save(os.path.join('flaskblog\\static\\blog_images', filename))

    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        print(file_path)
        post.blog_image=file_path
        
        db.session.commit()
        flash(f'Your Blog has been updated!', 'success')
        return redirect(url_for('posts.view_blog', post_id=post.id))

    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content


    return render_template('update_blog.html', title='Update Blog', form=form, post_id=post_id)



@posts.route("/blog/delete/<int:post_id>",methods=['POST'])
@login_required
def delete_blog(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash(f'Your Blog has been deleted!', 'success')
    return redirect(url_for('main.home'))
