'''Authentication Page Routing'''
from flask import Blueprint, render_template, abort, request, redirect, url_for, flash
from jinja2 import TemplateNotFound
from time import time as tme
from flask_login import login_user, login_required, logout_user, current_user
from . import db
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)


@auth.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@auth.route('/login', methods=['GET', 'POST'])
def login_page():
    rand_img = (int(str(tme()*1000)[-1]) % 4)+1
    try:
        if request.method == 'GET':
            return render_template('login.html', bg_img=rand_img)
        if request.method == 'POST':
            email = request.form.get('user')
            if email.count('@') == 1:
                user = User.query.filter_by(email=email).first()
            else:
                user = User.query.filter_by(username=email).first()
            password = request.form.get('passwd')
            remember = request.form.get('remember')
            if user:
                if check_password_hash(user.password, password):
                    flash('You have been logged in!', category='success')
                    print(remember)
                    if remember == 'on':
                        login_user(user, remember=True)
                    else:
                        login_user(user, remember=False)
                    return redirect(url_for('pages.home_page'))
                else:
                    flash('Incorrect password, please try again', category='error')
            else:
                flash("Email or Username doesn't exist!", category='error')
        return render_template("login.html", bg_img=rand_img)
    except TemplateNotFound:
        abort(404)


@auth.route('/register', methods=['GET', 'POST'])
def register_page():
    rand_img = (int(str(tme()*1000)[-1]) % 4)+1
    if request.method == 'GET':
        return render_template('register.html', bg_img=rand_img)
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstname')
        last_name = request.form.get('lastname')
        username = request.form.get('username')
        password = request.form.get('passwd')
        password_confirm = request.form.get('passwdconfirmed')
        email_check = User.query.filter_by(email=email).first()
        user_check = User.query.filter_by(username=username).first()
        if email_check:
            flash('Email already exist', category='error')
        elif user_check:
            flash(
                f'Your username, {username} was already taken', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 characters.', category='error')
        elif password != password_confirm:
            flash('Both passwords must be the same.', category='error')
        elif len(password) < 7:
            flash('Password must be at least 7 characters long.', category='error')
        else:
            if len(last_name) > 0:
                new_user = User(username=username, email=email, first_name=first_name,
                                last_name=last_name, password=generate_password_hash(password, method='sha384'))
            else:
                new_user = User(username=username, email=email, first_name=first_name,
                                password=generate_password_hash(password, method='sha384'))
            db.session.add(new_user)
            db.session.commit()
            flash('Account created!', category='success')
            return redirect(url_for('auth.login_page'))

        return render_template('register.html', bg_img=rand_img)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have logged out!', category='success')
    return redirect(url_for('auth.login_page'))



@auth.route('/about')
def about_page():
    return render_template('about.html')
