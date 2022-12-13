from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user

pages = Blueprint('pages', __name__)

@pages.route('/')
def home_page():
    if current_user.is_authenticated:
        return redirect(url_for('core.note_home'))
    return render_template('home.j2')
