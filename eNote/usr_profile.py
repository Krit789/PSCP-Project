from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from time import time as tme
from . import db
from .scrypt_hashing import generate_password_hash, check_password_hash
from .models import User, Note
import secrets

profile = Blueprint('profile', __name__)

def rand_img() -> int:
    return (int(str(tme()*1000)[-1]) % 9)+1

@profile.route('/user', methods=['GET', 'POST'])
@login_required
def user_profile():
    if request.method == 'GET':
        temp = current_user
        user_data = [temp.id, temp.username, temp.first_name, temp.last_name, str(temp.creation_date)[:19] + ' UTC', temp.theme, temp.total_notes, temp.deleted_notes]
        return render_template("profile.html", bg_img=rand_img(), user_data=user_data)
    if request.method == 'POST':
        delete = True if request.form.get('delete') == 'Delete Account' else False
        if delete:
            account = User.query.filter_by(id=current_user.id).one()
            notes = Note.query.filter_by(user_id=current_user.id)
            db.session.delete(account)
            db.session.delete(notes)
            db.session.commit()
            flash('Account deleted!', category='success')
        return redirect(url_for('pages.home_page'))


@profile.route('/user/edit', methods=['GET', 'POST'])
@login_required
def editor():
    if request.method == 'GET':
        temp = current_user
        user_data = [temp.id, temp.username, temp.first_name, temp.last_name, temp.email]
        return render_template("profile_edit.html", bg_img=rand_img(), user_data=user_data)
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstname')
        last_name = request.form.get('lastname')
        username = request.form.get('username')
        password = request.form.get('passwd')
        email_check = User.query.filter_by(email=email).first()
        user_check = User.query.filter_by(username=username).first()
        if email_check and email != current_user.email:
            flash('Email already exist', category='error')
        elif user_check and username != current_user.username:
            flash(
                f'Your username, {username} was already taken', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 characters.', category='error')
        else:
            if check_password_hash(email_check.password_hash, password, email_check.password_salt):
                updated_user = User.query.filter_by(id=current_user.id).first()
                updated_user.username = username
                updated_user.email = email
                updated_user.first_name = first_name
                if len(last_name) > 0:
                    updated_user.last_name = last_name
                else:
                    updated_user.last_name = None
                db.session.commit()
                flash('Changes saved!', category='success')
                return redirect(url_for('profile.user_profile'))
            else:
                flash('Incorrect password, please try again', category='error')
        return redirect(url_for('profile.editor'))

@profile.route('/user/password', methods=['GET', 'POST'])
@login_required
def password():
    if request.method == 'GET':
        return render_template("change_passwd.html", bg_img=rand_img())
    if request.method == 'POST':
        old_pass = request.form.get('currentpass')
        newpass = request.form.get('newpass')
        confnewpass = request.form.get('confnewpass')
        if newpass == confnewpass:
            user = User.query.filter_by(id=current_user.id).first()
            if check_password_hash(user.password_hash, old_pass, user.password_salt):
                if old_pass != newpass:
                    password_salt = secrets.token_hex(16)
                    user_password = generate_password_hash(newpass, password_salt)
                    user.password_hash = user_password
                    user.password_salt = password_salt
                    if request.form.get('logout') == 'on':
                        user.session_token = secrets.token_hex(16)
                        db.session.commit()
                        flash('Changes saved and all sessions have been purged!', category='success')
                        return redirect(url_for('pages.home_page'))
                    flash('Changes saved!', category='success')
                    db.session.commit()
                    return redirect(url_for('profile.user_profile'))
                else:
                    flash('New password can\'t be the same as current password', category='error')
            else:
                flash('Incorrect password, please try again', category='error')
        else:
            flash('New Password and Confirm New Password must be the same!', category='error')
        return redirect(url_for('profile.password'))