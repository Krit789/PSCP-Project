'''Backend of <e>Note App'''
from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from sqlalchemy import desc
from . import db
from .models import Note, User
from .md_bleach import md_cleaner, bleach

core = Blueprint('core', __name__)

def rand_img() -> int:
    '''Get note background from database if NULL use #6'''
    if current_user.is_anonymous:
        return 6
    return current_user.note_bg if current_user.note_bg is not None else 6

@core.errorhandler(404)
def note_not_found(e):
    '''404 Error Handler'''
    flash('This note does not exist', category='error')
    if current_user.is_anonymous:
        return redirect(url_for('pages.home_page'))
    return redirect(url_for('core.note_home'))

@core.errorhandler(403)
def note_not_found(e):
    '''403 Error Handler'''
    flash('You don\'t have permission to access this note', category='error')
    if current_user.is_anonymous:
        return redirect(url_for('pages.home_page'))
    return redirect(url_for('core.note_home'))

@core.route('/note', methods=['GET', 'POST'])
@login_required
def note_home():
    '''Note Home Page'''
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
            return redirect(url_for('core.note_home'))
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
def note_view(note_id):
    '''Note Viewer'''
    user_note = Note.query.filter_by(id=note_id).first_or_404()
    note_owner = User.query.filter_by(id=user_note.user_id).first_or_404()
    if user_note.is_public:
        return render_template('note_view.j2', note=user_note, bg_img=rand_img(), public=user_note.is_public, owner=note_owner)
    if current_user.is_anonymous:
        abort(403)
    if user_note.user_id != current_user.id:
        abort(403)
    return render_template('note_view.j2', note=user_note, bg_img=rand_img(), public=user_note.is_public)

@core.route('/note/settings', methods=['GET', 'POST'])
@login_required
def note_settings():
    '''Note Background Changer'''
    this_user = User.query.filter_by(id=current_user.id).first_or_404()
    bg_img = 6
    if request.method == 'GET':
        if current_user.note_bg is None:
            bg_img = 6
        else:
            bg_img = current_user.note_bg
    if request.method == 'POST':
        if request.form.get('background') is None:
            flash('Nothing changes', category='info')
        elif request.form.get('background').isnumeric():
            if int(request.form.get('background')) > 14 or int(request.form.get('background')) <= 0:
                flash('Invalid Background', category='error')
            else:
                this_user.note_bg = request.form.get('background')
                db.session.commit()
                flash('Background changed!', category='success')
        else:
            flash('Unknown Failure', category='error')
        bg_img = current_user.note_bg
    return render_template("note_settings.j2", bg_img=bg_img)


@core.route('/note/edit', methods=['POST'])
@login_required
def editor():
    '''Note Editor'''
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
        if editor_type == 'share':
            user_note.is_public = False if user_note.is_public else True
            db.session.commit()
            note_link = f'<a onclick="copyToClipboard();" href="#" id="copyText" >' + str(request.base_url)[:-4] + str(user_note.id) + '</a><br /><span id="copyStatus">Click the link to copy to clipboard</span>'
            flash(f'Link Sharing has been {"<b>enabled</b>" if user_note.is_public else "<b>disabled</b>"} for <strong>{user_note.title}</strong> {"<br/>" if user_note.is_public else ""} {note_link if user_note.is_public else ""}', category='success_show' if user_note.is_public else 'success')
            return redirect(url_for('core.note_home'))
        if user_note.user_id != current_user.id:
            abort(403)
        if editor_type not in ('simple', 'full'):
            editor_type = "full"
    return render_template('note_editor.j2', note=user_note, bg_img=rand_img(), draft=False, editor=editor_type)
