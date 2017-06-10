"""
    Create APIs
"""

import random
import requests
from datetime import datetime

from flask import request
from flask import jsonify
from flask_restful import Resource
from flask_restful import Api
from sqlalchemy.exc import IntegrityError

from .main import app
from .main import db
from .models import Point


class TempApi(Resource):
    """ Dummy temperature api """
    def post(self):
        """ Generates random weekly maximum and minimum temp. value """
        dataset = []
        name_key = 'points[{}][pointName]'
        lat_key = 'points[{}][pointLatitude]'
        lng_key = 'points[{}][pointLongitude]'
        geolocations = request.form
        for i in range(int(len(geolocations)/3)):
            name = geolocations[name_key.format(i)]
            lat = geolocations[lat_key.format(i)][0]
            lng = geolocations[lng_key.format(i)][0]
            raw_data = self.fetch(lat, lng)
            data = self.parse(raw_data)

            dataset.append({'label':name, 'data':data})
        return dataset

    def fetch(self, lat, lng):
        """
        Makes request to app url with given parameters
        Returns the result as JSON
        """
        payload = {"key":app.config['FORECAST_API_KEY'], "lat":lat, "lng":lng}
        response = requests.get(app.config['FORECAST_API_URL'], params=payload)
        return response.json()['dailyForecastPeriods']

            
    def toDayOfWeek(self, date):
        return datetime(*(int(x) for x in date[:10].split("-"))).strftime('%A')

    def parse(self, dataset):
        new_set = []
        node = {'day': self.toDayOfWeek(dataset[0]['forecastDateLocalStr'])}
        for data in dataset:
            if self.toDayOfWeek(data['forecastDateLocalStr'][:11]) != node['day'][:11]:
                if data['isNightTimePeriod']:
                    node['minimum'] = data['temperature']
                else:
                    node['maximum'] = data['temperature']
                new_set.append(node)
                node = {'day': self.toDayOfWeek(data['forecastDateLocalStr'])}
            else:
                if data['isNightTimePeriod']:
                    node['minimum'] = data['temperature']
                else:
                    node['maximum'] = data['temperature']
        return new_set

class PointApi(Resource):
    """  """
    def get(self, point_name):
        """ """
        point = Point.query.filter_by(pointName=point_name).first()
        # basic model to json
        if point:
            json_point = self.serialize(point)
            return {'point':json_point}
        else:
            return {'point':None}

    def post(self, point_name):
        """ """
        try:
            if Point.query.filter_by(pointName=request.form['pointName']).first():
                point_query = Point.query.filter_by(pointName=request.form['pointName'])
                point_query.update({name:value for name, value in request.form.items()})
                db.session.commit()
                return self.serialize(point_query.first())
            else:
                point = Point(**{name:value for name, value in request.form.items()})
                db.session.add(point)
                db.session.commit()
                return self.serialize(point)

        except TypeError as could_not_create:
            db.session.rollback()
            return {'error':"Invalid Arguments!"}
        except IntegrityError as could_not_save:
            db.session.rollback()
            return {'error':"Point already exists!"}

    def delete(self, point_name):
        """ """
        try:
            point = Point.query.filter_by(pointName=point_name).first()
            db.session.delete(point)
            db.session.commit()
            point = Point.query.filter_by(pointName=point_name).first()
            if point:
                return {"error":"could not delete"}
            else:
                return {"status":"success"}

        except TypeError:
            return {'error':"Invalid Arguments!"}
        except IntegrityError:
            return {"error":"could not delete"}

    def serialize(self, point):
        """ Basic model to json """
        return {name:value for name, value in vars(point).items() if isinstance(value, (str, float, int))}

class PointListApi(Resource):
    """ """
    def get(self):
        """ """
        points = Point.query.all()
        # basic model to json
        if points:
            json_points = [{name:value for name, value in vars(point).items() if type(value) in (str, float, int)} for point in points]
            return {'point':json_points}
        else:
            return {'point':None}
            
if not __name__ == "__main__":
    api = Api(app)
    api.add_resource(TempApi, "/api/temp")
    api.add_resource(PointListApi, "/api/point/")
    api.add_resource(PointApi, '/api/point/<point_name>')
