from flask import Blueprint, render_template, abort, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from time import time as tme
from . import db
from .models import User

pages = Blueprint('pages', __name__)

@pages.route('/')
def home_page():
    return render_template('home.html')

@pages.route('/user')
@login_required
def user_profile():
    rand_img = (int(str(tme()*1000)[-1]) % 4)+1
    # user_data = User.query.filter_by(id=current_user.get_id()).first()
    user_data = User.query.filter_by(id=int(current_user.get_id())).first()
    print(user_data)
     # ...
    return render_template("profile.html", bg_img=rand_img)
