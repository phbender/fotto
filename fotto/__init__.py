from flask import Flask
from flask.ext.mongoengine import MongoEngine
from flask.ext.login import LoginManager

app = Flask(__name__)
app.config.from_object('config')
db = MongoEngine(app)
login_manager = LoginManager()
login_manager.init_app(app)

from exif import exifdata as exifdata
from exif import imageinfo as imageinfo

from fotto.models import *
from fotto.views import *
