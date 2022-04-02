from flask import Blueprint, render_template, request
from client.forms import NoteRemoveForm
from models import Note
index_bp = Blueprint('index', __name__)


@index_bp.get('/')
def index_view():
    user_notes = Note.query.filter_by(owner=request.environ['user'].id).all()
    request.environ['user_notes'] = reversed(user_notes)
    request.environ['note_remove_form'] = NoteRemoveForm()
    return render_template('index.html')
