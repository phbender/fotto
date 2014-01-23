from fotto import app
from fotto.models import *

from flask import render_template, jsonify
from flask.views import MethodView
from flask.helpers import NotFound, send_file

def json_response(json_string):
    """Use this method if JSON is already serialized (and no longer a dict)"""
    return app.response_class(json_string, mimetype='application/json')

@app.route('/')
def index():
    return "Hello, fotto!"

@app.route('/views/<view_id>')
def view(view_id):
    the_view = View.objects(slug=view_id).first_or_404()
    return json_response(the_view.to_json())

@app.route('/views/<view_id>/<int:seq_num>')
def view_image(view_id, seq_num):
    the_view = View.objects(slug=view_id).first_or_404()
    try:
        the_image = the_view.images[seq_num]
        return send_file(the_image.image_data, mimetype=the_image.image_data.content_type)
    except IndexError, TypeError:
        # seq_num is invalid somehow
        raise NotFound







