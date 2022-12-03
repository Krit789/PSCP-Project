from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from sqlalchemy import desc
from . import db
from time import time as tme
from .models import Note, User
import bleach

core = Blueprint('core', __name__)

def rand_img() -> int:
    # return (int(str(tme()*1000)[-1]) % 9) + 1
    return 6

def md_cleaner(text: str) -> str:
    ALLOWED_TAGS = [
    "h1", "h2", "h3", "h4", "h5", "h6", "hr",
    "ul", "ol", "li", "p", "br",
    "pre", "code", "blockquote",
    "strong", "em", "a", "img", "b", "i",
    "table", "thead", "tbody", "tr", "th", "td",
    ]
    ALLOWED_ATTRIBUTES = {
        "h1": ["id"], "h2": ["id"], "h3": ["id"],  "h4": ["id"],
        "a": ["href", "title"],
        "img": ["src", "title", "alt"],
    }
    ALLOWED_PROTOCOLS = ["http", "https", "mailto"]
    cleaner = bleach.Cleaner(
                tags=ALLOWED_TAGS,
                attributes=ALLOWED_ATTRIBUTES,
                protocols=ALLOWED_PROTOCOLS)
    return cleaner.clean(text)

@core.errorhandler(404)
@login_required
def note_not_found(e):
    flash('This note does not exist', category='error')
    return redirect(url_for('core.note_home'))

@core.errorhandler(403)
@login_required
def note_not_found(e):
    flash('You don\'t have permission to access this note', category='error')
    return redirect(url_for('core.note_home'))

@core.route('/note', methods=['GET', 'POST'])
@login_required
def note_home():
    if request.method == 'GET':
        user_note = Note.query.filter_by(user_id=current_user.id).order_by(desc(Note.last_edit))
        return render_template("note.j2", all_note=user_note, bg_img=rand_img())
    if request.method == 'POST':
        action = request.form.get('action')
        this_user = User.query.filter_by(id=current_user.id).first()
        if action == 'create':
            if request.form.get('title') is None and request.form.get('editor_type') == 'blank':
                title = "Untitled Note"
                note_content = ""
            elif len(request.form.get('title')) == 0:
                title = "Untitled Note"
                note_content = md_cleaner(request.form.get('content'))
            else:
                title = bleach.clean(request.form.get('title'))
                note_content = md_cleaner(request.form.get('content'))
            memo = Note(title=title, content=note_content, user_id=current_user.id)
            this_user.total_notes = int(this_user.total_notes) + 1
            db.session.add(memo)
            db.session.commit()
            flash(f'<b>{title}</b> was created successfully!', category='success')
            return redirect(url_for('core.note_home', bg_img=rand_img()))
        user_note = Note.query.filter_by(id=request.form.get('note_id')).first_or_404()
        if user_note.user_id != current_user.id:
            abort(403)
        if action == 'update':
            if user_note.content != md_cleaner(request.form.get('content')) or user_note.title != bleach.clean(request.form.get('title')):
                user_note.content = md_cleaner(request.form.get('content'))
                user_note.title = bleach.clean(request.form.get('title'))
                db.session.commit()
                flash(f'Changes saved to <b>{user_note.title}</b>', category='success')
            else:
                flash(f'Changes not saved to <b>{user_note.title}</b> due to no changes')
            return redirect(url_for('core.note_view', note_id=user_note.id, bg_img=rand_img()))
        if action == 'delete':
            title = user_note.title
            this_user.deleted_notes = int(this_user.deleted_notes) + 1
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
    return render_template('note_view.j2', note=user_note, bg_img=rand_img())

@core.route('/note/edit', methods=['POST'])
@login_required
def editor():
    editor_type = request.form.get('editor_type')
    note_id = request.form.get('note_id')
    if note_id is None and editor_type is not None:
        if editor_type == 'blank':
            return redirect(url_for('core.note_home'), code=307)
        placeholder = Note(title="", content="", id=0, creation_date="Not saved yet", last_edit="Not saved yet")
        if editor_type in ('simple', 'full'):
            flash("This note is a draft. <strong>Changes will not be save</strong> until you click save", category='warning')
            return render_template('note_editor.j2', note=placeholder, bg_img=rand_img(), draft=True, editor=editor_type)
    elif note_id is not None:
        user_note = Note.query.filter_by(id=note_id).first_or_404()
        if user_note.user_id != current_user.id:
            abort(403)
        if editor_type not in ('simple', 'full'):
            editor_type = "full"
    return render_template('note_editor.j2', note=user_note, bg_img=rand_img(), draft=False, editor=editor_type)
