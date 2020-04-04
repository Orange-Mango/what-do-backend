from http import HTTPStatus

from flask import abort, jsonify, request, make_response

from . import app, db
from .models import Activity
from .models import Tag


@app.route('/', methods=('GET',))
def index():
    return jsonify('Hello, World!')

@app.route('/activities', methods=('GET',))
def activities_index():
    activities = Activity.query.all()
    return jsonify([
        {
            'description': activity.description,
            'id': activity.id,
            'tags':activity.tags
        }
        for activity in activities
    ])

@app.route('/activities', methods=('POST',))
def activities_create():
    if not request.is_json:
        abort(HTTPStatus.UNSUPPORTED_MEDIA_TYPE)
    data = request.json
    if set(data.keys()) != {'description','tags'}:
        abort(HTTPStatus.BAD_REQUEST)
    activity = Activity(description=data['description'])
    for n in data['tags']:
        activity.tags.append(
            Tag(name=n)
        )
    db.session.add(activity)
    db.session.commit()
    return make_response('', HTTPStatus.CREATED)

@app.route('/tags', methods=('GET',))
def tags_index():
    tags = Tag.query.all()
    return jsonify([
        {
            'name': tag.name,
            #'id': tag.id,
            'activities': tag.activities
        }
        for tag in tags
    ])

@app.route('/tags', methods=('POST',))
def tags_create():
    if not request.is_json:
        abort(HTTPStatus.UNSUPPORTED_MEDIA_TYPE)
    data = request.json
    if set(data.keys()) != {'name'}:
        abort(HTTPStatus.BAD_REQUEST)
    tag = Tag(name=data['name'])
    db.session.add(tag)
    db.session.commit()
    return make_response('', HTTPStatus.CREATED)