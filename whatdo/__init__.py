from flask import Flask, jsonify
from flask.app import HTTPException


app = Flask(__name__)

@app.errorhandler(HTTPException)
def handle_http_exception(e):
    return jsonify(code=e.code, description=e.description), e.code

import whatdo.views
