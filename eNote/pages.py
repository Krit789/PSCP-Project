from flask import Blueprint, render_template, abort, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from time import time as tme
from . import db
from .models import User

pages = Blueprint('pages', __name__)

@pages.route('/')
def home_page():

    return render_template('home.html')

@pages.route('/user', methods=['GET', 'POST'])
@login_required
def user_profile():
    rand_img = (int(str(tme()*1000)[-1]) % 4)+1
    # user_data = User.query.filter_by(id=current_user.get_id()).first()
    if request.method == 'GET':
        temp = current_user
        user_data = [temp.id, temp.username, temp.first_name, temp.last_name, temp.creation_date]
        return render_template("profile.html", bg_img=rand_img, user_data=user_data)
    if request.method == 'POST':
        delete = True if request.form.get('delete') == 'Delete Account' else False
        if delete:
            obj = User.query.filter_by(id=current_user.id).one()
            db.session.delete(obj)
            db.session.commit()
            flash('Account deleted!', category='success')
        return redirect(url_for('pages.home_page'))