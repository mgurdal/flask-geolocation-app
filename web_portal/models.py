"""
Create database models here.
"""
from flask_sqlalchemy import SQLAlchemy
from .main import db

class Point(db.Model):
    '''
    Extend `db.Model`. Database model representing a point in map.

    Attributes:
        id (:Column:`int`): Primary key field.
        pointName (:Column:`str`): The name of the point.
        pointLatitude (:Column:`float`): The latitude value for the point.
        pointLongitude (:Column:`float`): The longitude value for the point.
    '''
    id = db.Column(db.Integer, primary_key=True)
    pointName = db.Column(db.String(120), unique=True)
    pointLatitude = db.Column(db.FLOAT())
    pointLongitude = db.Column(db.FLOAT())

    def __init__(self, pointName, pointLatitude, pointLongitude):
        ''' Initialize the point attributes.''' 
        self.pointName = pointName
        self.pointLatitude = pointLatitude
        self.pointLongitude = pointLongitude
