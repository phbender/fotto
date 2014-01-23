from fotto import app

from flask import render_template, jsonify
from flask.views import MethodView

def json_response(json_string):
    """Use this method if JSON is already serialized (and no longer a dict)"""
    return app.response_class(json_string, mimetype='application/json')

@app.route('/')
def index():
    return "Hello, fotto!"

