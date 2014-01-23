#!/usr/bin/env python

from flask.ext.script import Manager
from fotto import app, db

import os.path

manager = Manager(app)

if __name__ == '__main__':
    manager.run()
