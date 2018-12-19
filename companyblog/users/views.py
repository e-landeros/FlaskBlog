from flask import render_template, url_for, redirect, flash, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from companyblog import db
from companyblog.models import User, BlogPost
from companyblog.users.forms import RegistrationForm, LoginForm, UpdateUserForm
from companyblog.users.picture_handler import add_profile_pic

users = Blueprint('users', __name__)

#register user
@users.route('/register', methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_sumbit():
        user = User(email=form.email.data,
                 username=form.username.data,
                 password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Thanks for Registration')
        return redirect(url_for('users.login'))
    return render_template('register.html', form=form)

#login user
@users.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_sumbit():
        user = User.query.filter_by(email=form.email.data).first()
        if user.check_password(form.password.data) and user is not None:
            login_user(user)
            flash('Login Success')

            next = request.args.get('next')#grab the page user was trying to access from the requests session so i can redirect them
            if next == None or not next[0]=='/'
                next = url_for('core.index')
            return redirect(next)
    return render_template('login.html', form=form)

#logout user
@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('core.index'))

#account(update UserForm)
@users.route('/account', methods=['GET','POST'])
@login_required
def account():
    form = UpdateUserForm()
    if form.validate_on_sumbit():
        #if they uploaded pic FileField
        if form.picture.data:
            username = current_user.username
            pic = add_profile_pic(form.picture.data,username)
            current_user.profile_image = pic
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('User Account Updated')
        return redirect(url_for('users.account'))

    #not submitting anything we get their current info from form
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    profile_image = url_for('static', filename='profile_pics/'+current_user.profile_image)
    return render_template('account.html', profile_image=profile_image, form=form)

#show all list of users blog post
@users.route('/<username>')
def user_posts(username):
    page = request.args.get('page',1,type=int)