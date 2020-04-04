from flask import Flask, jsonify
from flask.app import HTTPException
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)  # pylint:disable=C0103

app.config.from_envvar('WHATDO_SETTINGS', silent=True)


@app.errorhandler(HTTPException)
def handle_http_exception(ex):
    return jsonify(code=ex.code, description=ex.description), ex.code


db = SQLAlchemy(app)  # pylint:disable=C0103
import whatdo.models  # pylint:disable=C0413,R0401 # noqa:E402
db.create_all()

if app.config.get('CORS_ORIGINS'):
    CORS(app)

import whatdo.views  # pylint:disable=C0413,R0401 # noqa:E402,F401
