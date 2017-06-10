"""
Manage the application
"""

import decimal
import json
import datetime

from flask import Flask, request
from flask import render_template

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import DeclarativeMeta

app = Flask(__name__,  static_url_path='/static')
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)
from views import *

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True, use_reloader=True)