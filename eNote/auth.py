'''Authentication Page Routing'''
from flask import Blueprint, render_template, request, redirect, url_for, flash
from time import time as tme
from flask_login import login_user, login_required, logout_user, current_user
from . import db
from .models import User
import secrets
from hashlib import scrypt

auth = Blueprint('auth', __name__)

def check_password_hash(stored_key: str, password: str, password_salt: str) -> bool:
    if scrypt(password.encode(), salt=password_salt.encode(), n=16384, r=8, p=1, dklen=64) == stored_key:
        return True
    return False


@auth.route('/login', methods=['GET', 'POST'])
def login_page():
    if current_user.is_anonymous:
        rand_img = (int(str(tme()*1000)[-1]) % 10)+1
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
                if check_password_hash(user.password_hash, password, user.password_salt):
                    flash('You have been logged in!', category='success')
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
    else:
        flash('You have already logged in!', category='warning')
        return redirect(url_for('pages.home_page'))

@auth.route('/register', methods=['GET', 'POST'])
def register_page():
    if current_user.is_anonymous:
        rand_img = (int(str(tme()*1000)[-1]) % 9)+1
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
                user_salt = secrets.token_hex(32)
                user_password = scrypt(password.encode(), salt=user_salt.encode(), n=16384, r=8, p=1, dklen=64)
                new_user = User(username=username, session_token=secrets.token_hex(16), email=email, first_name=first_name,
                                password_hash=user_password, password_salt=user_salt)
                if len(last_name) > 0:
                    new_user.last_name = last_name
                else:
                    new_user.last_name = None
                db.session.add(new_user)
                db.session.commit()
                flash('Account created!', category='success')
                return redirect(url_for('auth.login_page'))
            return render_template('register.html', bg_img=rand_img)
    else:
        flash('You have already logged in!', category='warning')
        return redirect(url_for('pages.home_page'))

@auth.route('/logoutall')
@login_required
def logout_all():
    user = User.query.filter_by(id=current_user.id).first()
    user.session_token = secrets.token_hex(16)
    db.session.commit()
    logout_user()
    flash('You have been logged out of all session', category='talert')
    return redirect(url_for('auth.login_page'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have logged out!', category='talert')
    return redirect(url_for('auth.login_page'))


