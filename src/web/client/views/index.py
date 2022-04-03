from flask import Blueprint, render_template, request, request_tearing_down
from client.forms import NoteRemoveForm,NoteCreateForm
from models import Note
index_bp = Blueprint('index', __name__)


@index_bp.get('/')
def index_view():
    if request.environ['user'] is None:
        return render_template('index.html')
    else:
        user_notes = Note.query.filter_by(owner=request.environ['user'].id).all()
        request.environ['user_notes'] = reversed(user_notes)
        request.environ['note_remove_form'] = NoteRemoveForm()
        return render_template('home.html')
