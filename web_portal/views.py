"""
Create views
"""

from flask import render_template
from flask import request

from main import app, db
from .models import Point
from . import api

@app.route('/', methods=['GET',])
def index():
    """ Initializes index page variables """
    points = Point.query.order_by('pointName').all()
    template_name = 'index.html'
    return render_template(template_name, points=points, maps_api_key=app.config['GOOGLEMAPS_KEY'])

@app.route('/data_template', methods=['GET',])
def index_ajax():
    """ Allows us to make XHR """
    points = Point.query.order_by('pointName').all()
    template_name = 'index_ajax.html'
    return render_template(template_name, points=points)
