from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from . import db
from .models import User, Note

core = Blueprint('core', __name__)

@core.route('/note', methods=['GET', 'POST'])
@login_required
def note_home():
    if request.method == 'GET':
        user_note = Note.query.filter_by(user_id=current_user.id)
        return render_template("note.html", all_note=user_note)
    if request.method == 'POST':
        action = request.form.get('action')
        title_n = request.form.get('title')
        content = request.form.get('content')
        if action == 'create_note':
            memo = Note(title=title_n, content=content, user_id=current_user.id)
            db.session.add(memo)
            db.session.commit()
            flash('Note Created Successfully!', category='success')
    return redirect(url_for('core.note_home'))

@core.route('/note/<int:note_id>')
@login_required
def note_view(note_id):
    user_note = Note.query.filter_by(id=note_id).first_or_404()
    if user_note.user_id != current_user.id:
        abort(403)
    return render_template('note_view.html', note=user_note)