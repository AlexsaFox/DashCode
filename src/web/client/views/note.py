from flask import Blueprint, redirect, render_template, url_for, flash, request
from .auth import authorization_required
from models import Note, db_add, db_remove, db_save_changes
from client.forms import NoteCreateForm, NoteEditForm, NoteRemoveForm,flash_errors
note_bp = Blueprint('note',__name__)

def get_note_by_id(note_id: str) -> Note:
    ''' Returns instance of note from database using UUID '''
    return Note.query.filter_by(id=note_id).first()

@note_bp.get('/')
@authorization_required
def notes_show():
    # User.query.filter_by(username=form.data['username_or_email']).first() or
    user_notes = Note.query.filter_by(user=request.environ['user']).all()
    request.environ['user_notes'] = reversed(user_notes)
    request.environ['note_remove_form'] = NoteRemoveForm()
    return render_template("note/index.html")
@note_bp.get('/<note_id>')
def notes_show_handler(note_id):
    note = get_note_by_id(note_id)
    request.environ['note'] = note
    return render_template("note/note_show.html")

@note_bp.get('/create')
@authorization_required
def notes_create():
    request.environ['form'] = NoteCreateForm()
    return render_template("note/note_create.html")

@note_bp.post('/create')
@authorization_required
def notes_create_handle():
    request.environ['form'] = form = NoteCreateForm()
    if not form.validate():
        flash_errors(form)
        return render_template("note/note_create.html")
    user = request.environ['user']
    note = Note(
        title=form.data['title'],
        context=form.data['context'],
        link=form.data['link'],
        owner_id=user.id
    )
    db_add(note)
    return redirect(url_for('webapp.note.notes_show'))

@note_bp.get('/edit/<note_id>')
@authorization_required
def notes_edit(note_id):
    note = get_note_by_id(note_id)
    request.environ['note_id'] = note.id
    request.environ['form'] = NoteEditForm()
    request.environ['form'].title.data = note.title
    request.environ['form'].context.data = note.context
    request.environ['form'].link.data = note.link
    if note.is_private == True:
        request.environ['form'].privacy.data = request.environ['form'].privacy.choices[0][0]
    else:
        request.environ['form'].privacy.data = request.environ['form'].privacy.choices[1][0]
    return render_template("note/note_edit.html")

@note_bp.post('/edit/<note_id>')
@authorization_required
def notes_edit_handler(note_id):
    note = get_note_by_id(note_id)
    request.environ['form'] = form = NoteEditForm() 
    if not form.validate():
        flash_errors(form)
        return render_template("note/note_edit.html")
    if note is not None:
        note.title = form.data['title']
        note.context = form.data['context']
        note.link = form.data['link']
        if form.data['privacy'] == 'private':
            note.is_private = True
        else:
            note.is_private = False
        db_save_changes()
    return redirect(url_for('webapp.note.notes_show'))

@note_bp.post('/delete/<note_id>')
@authorization_required
def notes_remove_handler(note_id):
    request.environ['form'] = form = NoteRemoveForm()
    if not form.validate():
        flash_errors(form)
        return redirect("note/index.html")
    note = get_note_by_id(note_id)
    if note is not None:
        db_remove(note)
    return redirect(url_for('webapp.note.notes_show'))

