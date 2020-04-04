from http import HTTPStatus

from flask import abort, jsonify, request, session, make_response

from . import app, db
from . import service
from .auth import GoogleUser
from .models import Activity, User


@app.route('/', methods=('GET',))
def index():
    return jsonify('Hello, World!')


@app.route('/activities/<int:act_id>/like', methods=('PUT',))
def activity_like(act_id):
    found = service.activity_like(act_id)
    if not found:
        return make_response('', HTTPStatus.NOT_FOUND)
    return make_response('', HTTPStatus.NO_CONTENT)


@app.route('/activities', methods=('GET',))
def activities_index():
    activities = Activity.query.all()
    return jsonify([
        {
            'description': activity.description,
            'id': activity.id,
            'score': activity.score,  # TODO: remove later. this too -> # pylint:disable=W0511 # noqa:E501
            'tags': [
                {'name': tag.name, 'id': tag.id, }
                for tag in activity.tags
            ]
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


@app.route('/auth/login', methods=('POST',))
def auth_login():
    if not request.is_json:
        abort(HTTPStatus.UNSUPPORTED_MEDIA_TYPE)
    try:
        google_user = GoogleUser.from_token(
            (request.json or {}).get('idtoken'),
            app.config['GOOGLE_CLIENT_ID'])
    except ValueError:
        abort(HTTPStatus.UNAUTHORIZED)
    user = User.query.filter_by(google_id=google_user.id).first()
    new_user = user is None
    if new_user:
        user = User(google_id=google_user.id, name=google_user.given_name)
        db.session.add(user)
        db.session.commit()
    session['user_id'] = user.id
    return (jsonify({'id': user.id, 'name': user.name}),
            HTTPStatus.CREATED if new_user else HTTPStatus.OK)


@app.route('/auth/logout', methods=('POST',))
def auth_logout():
    session.clear()
    return '', HTTPStatus.NO_CONTENT
