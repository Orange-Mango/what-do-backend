from http import HTTPStatus

from flask import abort, jsonify, request, make_response

from . import app, db
from . import service
from .models import Activity


@app.route('/', methods=('GET',))
def index():
    return jsonify('Hello, World!')


@app.route('/activities/<int:act_id>/like', methods=('PUT',))
def activity_like(act_id):
    found = service.activity_like(act_id)
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
    if set(data.keys()) != {'description'}:
        abort(HTTPStatus.BAD_REQUEST)
    activity = Activity(description=data['description'])
    db.session.add(activity)
    db.session.commit()
    return make_response('', HTTPStatus.CREATED)


def activities_to_json(activities):
    return jsonify([
        {
            'description': activity.description,
            'id': activity.id,
            'created': activity.created,
            'score': "{:.2f}".format(activity.score),  # TODO remove later
            'tags': [
                {'name': tag.name, 'id': tag.id, }
                for tag in activity.tags
            ]
        }
        for activity in activities
    ])
