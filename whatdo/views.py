from http import HTTPStatus

from flask import abort, jsonify, request, make_response

from . import app, db
from .models import Activity
from . import service

@app.route('/', methods=('GET',))
def index():
    return jsonify('Hello, World!')

@app.route('/activities/<int:id>/like', methods=('PUT',))
def activity_like(id):
    found = service.activity_like(id)
    if(not found):
        return make_response('', HTTPStatus.NOT_FOUND)

    return make_response('', HTTPStatus.NO_CONTENT)

@app.route('/activities', methods=('GET',))
def activities_index():
    activities = Activity.query.all()
    return jsonify([
        {
            'description': activity.description,
            'id': activity.id,
            'score' : activity.score # TODO remove later
        }
        for activity in activities
    ])

@app.route('/activities', methods=('POST',))
def activities_create():
    if not request.is_json:
        abort(HTTPStatus.UNSUPPORTED_MEDIA_TYPE)
    data = request.json
    if set(data.keys()) != {'description'}:
        abort(HTTPStatus.BAD_REQUEST)
    activity = Activity(description=data['description'])
    db.session.add(activity)
    db.session.commit()
    return make_response('', HTTPStatus.CREATED)