from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

core = Blueprint('core', __name__)

@core.route('/note')
@login_required
def note_home():
    return 'eNote Core'