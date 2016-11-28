from app import server
from app.user import api as user_api
from app.knowledge import api as knowledge_api

from flask import render_template, make_response, request

@server.route('/')
def hello():
    return render_template('index.html', isNew=True, note_id=-1)


@server.route('/docs', methods=['GET'])
def load_editor():
    # TODO: validate user identity
    try:
        note_id = request.args['note_id']
    except KeyError:
        return make_response("No note id")
    return render_template('index.html', isNew=False, note_id=note_id)


@server.route('/notes')
def notes_page():
    return render_template('notes_page.html')
