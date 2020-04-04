from http import HTTPStatus

from flask import abort, jsonify, request, make_response

from . import app, db
from . import service
from .models import Activity
from .models import Tag


@app.route('/', methods=('GET',))
def index():
    return jsonify('Hello, World!')


@app.route('/activities/<int:id>/like', methods=('PUT',))
def activity_like(id):
    found = service.activity_like(id)
    if not found:
        abort(HTTPStatus.NOT_FOUND)
    return make_response('', HTTPStatus.NO_CONTENT)


@app.route('/activities', methods=('GET',))
def activities_index():
    activities = Activity.query.all()
    return activities_to_json(activities)


@app.route('/activities/ordered', methods=('GET',))
def activities_ordered():
    exclude_activities = request.args.getlist('not')
    if not isinstance(exclude_activities, list):
        abort(HTTPStatus.BAD_REQUEST)

    activities = service.get_activities_ordered(exclude_activities)
    return activities_to_json(activities)

@app.route('/activities', methods=('POST',))
def activities_create():
    if not request.is_json:
        abort(HTTPStatus.UNSUPPORTED_MEDIA_TYPE)
    data = request.json
    if set(data.keys()) != {'description','tags'}:
        abort(HTTPStatus.BAD_REQUEST)
    tags_list = []
    for name in data['tags']:
        if Tag.query.filter_by(name=name).first():
                tags_list.append(Tag.query.filter_by(name=name).first())
        else:
            abort(HTTPStatus.BAD_REQUEST)
    activity = Activity(description=data['description'],tags=tags_list)
    db.session.add(activity)
    db.session.commit()
    return make_response('', HTTPStatus.CREATED)

@app.route('/tags', methods=('GET',))
def tags_index():
    tags = Tag.query.all()
    return jsonify([
        {
            'name': tag.name,
            'activities': [
                {'description': activity.description}
                for activity in tag.activities
                ]
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

@app.route("/activity/<int:id>", methods=('DELETE',))
def activity_delete(id):
    found = service.activity_delete(id)
    if not found:
        pass
        abort(HTTPStatus.NOT_FOUND)

    return make_response('', HTTPStatus.NO_CONTENT)


def activities_to_json(activities):
    return jsonify([
        {
            'description': activity.description,
            'id': activity.id,
            'created': activity.created,
            'score': "{:.2f}".format(activity.score),  # TODO remove later
            'tags':[
                {'name': tag.name }
                for tag in activity.tags
                ]   
        }
        for activity in activities
    ])
