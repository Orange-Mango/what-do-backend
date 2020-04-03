from flask import Flask, jsonify
from flask.app import HTTPException
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config.from_envvar('WHATDO_SETTINGS', silent=True)

@app.errorhandler(HTTPException)
def handle_http_exception(e):
    return jsonify(code=e.code, description=e.description), e.code

db = SQLAlchemy(app)
import whatdo.models
db.create_all()

if app.config.get('CORS_ORIGINS'):
    CORS(app)

import whatdo.views
