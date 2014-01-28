from fotto import app
from fotto.models import *

from flask import render_template, jsonify
from flask.views import MethodView
from flask.helpers import NotFound, send_file

def json_response(json_string):
    """Use this method if JSON is already serialized (and no longer a dict)"""
    return app.response_class(json_string, mimetype='application/json')

def collection_by(selector, identifier):
    if selector == "id":
        return Collection.objects(id=identifier).first_or_404()
    elif selector == "name":
        return Collection.objects(Q(slug=identifier) & Q(public=True)).first_or_404()
    else:
        raise NotFound

def collection_by_slug(slug):
    collection = Collection.objects(slug=slug).first_or_404()
    return collection

@app.route('/')
def index():
    return render_template('base.html')

@app.route('/collection/<selector>/<collection_id>/')
def collection(selector, collection_id):
    coll = collection_by(selector, collection_id)
    return render_template("collection_view.html", collection=coll)

@app.route('/collection/<selector>/<collection_id>/<int:seq_num>/<size>')
@app.route('/collection/<selector>/<collection_id>/<int:seq_num>')
def view_image(selector, collection_id, seq_num, size=None):
    coll = collection_by(selector, collection_id)
    try:
        the_image = coll.images[seq_num]
        return send_file(the_image.image_data, mimetype='image/jpeg')
    except IndexError, TypeError:
        # seq_num is invalid somehow
        raise NotFound







