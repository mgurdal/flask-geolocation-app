"""
Create views
"""

from flask import render_template
from flask import request

from myapp import app, db
from models import Point
import api

@app.route('/', methods=['POST', 'GET', 'PUT'])
def index():
    """ Initializes index page variables """
    points = Point.query.all()[::-1]
    if not points:
        db.session.add(Point(pointName='point_1', pointLatitude=37.2312, pointLongitude=36.231))
        db.session.commit()
        points = Point.query.all()[::-1]
    template_name = 'index.html'
    return render_template(template_name, points=points)

@app.route('/data_template', methods=['GET',])
def index_ajax():
    """ Allows us to make XHR """
    points = Point.query.all()[::-1]
    template_name = 'index_ajax.html'
    return render_template(template_name, points=points)
