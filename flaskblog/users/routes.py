from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from flaskblog import db, bcrypt
from flaskblog.models import User, Post
from flaskblog.users.forms import RegistrationForm, LoginForm, RequestResetForm, ResetPasswordForm, UpdateUserForm
from flaskblog.users.utils import save_user_image, send_reset_email


users = Blueprint('users', __name__)


@users.route("/register", methods=('GET', 'POST'))
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(name=form.name.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created successfully!', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)



@users.route("/login", methods=('GET', 'POST'))
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash(f'Login unsuccessfully!', 'danger')
            return redirect(url_for('users.login'))
    return render_template('login.html', title='Login',form=form)



@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))



@users.route("/account")
@login_required
def account():
    image_file = url_for('static', filename='profile_pics/default.jpg' )
    posts = Post.query.all()
    return render_template('account.html', title='Account', image_file=image_file, posts=posts)



@users.route("/updateaccount",methods=('GET', 'POST'))
@login_required
def updateaccount():
    form = UpdateUserForm()
    if form.validate_on_submit():
        if form.user_image.data:
            image_file = save_user_image(form.user_image.data)
            current_user.user_image = image_file
        current_user.name = form.name.data
        current_user.email = form.email.data
        db.session.commit()
        flash(f'Your account has been updated!', 'success')
        return redirect(url_for('users.updateaccount'))
    
    elif request.method=='GET':
        form.name.data = current_user.name
        form.email.data = current_user.email

    image_file = url_for('static', filename='profile_pics/default.jpg' )
    return render_template('updateaccount.html', title='Update Account', image_file=image_file, form=form)



@users.route("/user/profile/<name>")
def user_profile(name):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(name=name).first_or_404()
    posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(page=page, per_page=6)
    image_file = url_for('static', filename='profile_pics/default.jpg' )  #This is a static image for testing
    return render_template('user_profile.html', user=user, posts=posts, image_file=image_file)



@users.route("/request_reset",methods=('GET', 'POST'))
def request_reset():
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent to reset yor password.', 'info')
        return redirect(url_for('users.login'))
    return render_template('request_reset.html', form=form)



@users.route("/request_reset/<token>",methods=('GET', 'POST'))
def reset_password(token):

    user = User.verify_reset_token(token)

    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))

    

    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()

        flash(f'Your Password has been updated successfully!', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_password.html', form=form)
