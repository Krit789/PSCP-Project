from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

pages = Blueprint('pages', __name__)

@pages.route('/')
def home_page():
    if current_user.is_authenticated:
        return redirect(url_for('core.note_home'))
    return render_template('home.html')