from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from sqlalchemy import desc
from . import db
from time import time as tme
from .models import Note
import bleach

core = Blueprint('core', __name__)

def rand_img() -> int:
    # return (int(str(tme()*1000)[-1]) % 9) + 1
    return 6

@core.route('/note', methods=['GET', 'POST'])
@login_required
def note_home():
    if request.method == 'GET':
        user_note = Note.query.filter_by(user_id=current_user.id).order_by(desc(Note.last_edit))
        return render_template("note.html", all_note=user_note, bg_img=rand_img())
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'create':
            if len(request.form.get('title')) == 0:
                title = "Untitled Note"
            else:
                title = bleach.clean(request.form.get('title'))
            memo = Note(title=title, content=bleach.clean(request.form.get('content')), user_id=current_user.id)
            db.session.add(memo)
            db.session.commit()
            flash(f'<b>{title}</b> was Created Successfully!', category='success')
            return redirect(url_for('core.note_home', bg_img=rand_img()))
        user_note = Note.query.filter_by(id=request.form.get('note_id')).first_or_404()
        if user_note.user_id != current_user.id:
            abort(403)
        if action == 'update':
            user_note.title = bleach.clean(request.form.get('title'))
            if user_note.content != bleach.clean(request.form.get('content')):
                user_note.content = bleach.clean(request.form.get('content'))
                db.session.commit()
                flash(f'Changes saved to <b>{user_note.title}</b>', category='success')
            else:
                flash(f'Changes not saved to <b>{user_note.title}</b> due to no changes')
            return redirect(url_for('core.note_view', note_id=user_note.id, bg_img=rand_img()))
        if action == 'delete':
            title = user_note.title
            db.session.delete(user_note)
            db.session.commit()
            flash(f'<b>{title}</b> was deleted', category='success')
            return redirect(url_for('core.note_home', bg_img=rand_img()))

@core.route('/note/<int:note_id>')
@login_required
def note_view(note_id):
    user_note = Note.query.filter_by(id=note_id).first_or_404()
    if user_note.user_id != current_user.id:
        abort(403)
    return render_template('note_view.html', note=user_note, bg_img=rand_img())

@core.route('/note/edit', methods=['POST'])
@login_required
def editor():
    note_id = request.form.get('note_id')
    user_note = Note.query.filter_by(id=note_id).first_or_404()
    if user_note.user_id != current_user.id:
        abort(403)
    return render_template('note_editor.html', note=user_note, bg_img=rand_img())