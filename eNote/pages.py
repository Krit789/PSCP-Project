from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

pages = Blueprint('pages', __name__)

@pages.route('/')
def home_page():
    if current_user.is_authenticated:
        return redirect(url_for('core.note_home'))
    return render_template('home.html')

@pages.route('/about')
def about_page():
    return render_template('about.html')

@pages.route('/flash/<flash_t>')
def flash_test(flash_t):
    flash('This is a test', category=flash_t)
    return render_template('login.html')