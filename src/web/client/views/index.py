from flask import Blueprint, render_template, request, request_tearing_down
from client.forms import NoteRemoveForm,NoteCreateForm,NoteEditForm
from models import Note
index_bp = Blueprint('index', __name__)


@index_bp.get('/')
def index_view():
    if request.environ['user'] is not None:
        user_notes = Note.query.filter_by(user=request.environ['user']).all()
        request.environ['user_notes'] = reversed(user_notes)
        request.environ['note_remove_form'] = NoteRemoveForm()
        request.environ['note_create_form'] = NoteCreateForm()
        request.environ['note_edit_form'] = NoteEditForm()
        return render_template('home.html')
    return render_template('index.html')
