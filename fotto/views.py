from fotto import app
from fotto.models import *

from flask import render_template, jsonify
from flask.views import MethodView
from flask.helpers import NotFound, send_file

def json_response(json_string):
    """Use this method if JSON is already serialized (and no longer a dict)"""
    return app.response_class(json_string, mimetype='application/json')

def collection_by_id(collection_id):
    collection = Collection.objects(Q(slug=collection_id) | Q(id=collection_id)).first_or_404()
    return collection

@app.route('/')
def index():
    return "Hello, fotto!"

@app.route('/collection/<collection_id>/')
def collection(collection_id):
    coll = collection_by_id(collection_id)
    return json_response(coll.to_json())

@app.route('/collection/<collection_id>/<int:seq_num>')
def view_image(collection_id, seq_num):
    coll = collection_by_id(collection_id)
    try:
        the_image = coll.images[seq_num]
        return send_file(the_image.image_data, mimetype=the_image.image_data.content_type)
    except IndexError, TypeError:
        # seq_num is invalid somehow
        raise NotFound







