from flask import jsonify

from . import app


@app.route('/', methods=('GET',))
def index():
    return jsonify('Hello, World!')

@app.route('/activities')
def activities_index():
    return jsonify([
        {'text': 'Lorem ipsum dolor sit amet'},
        {'text': 'Consectetur adipiscing elit'},
        {'text': 'Sed venenatis mauris nisi'},
        {'text': 'Lacinia ex aliquet vel'},
        {'text': 'Ut ultricies diam in libero'},
    ])
