from myapp import app, db
from models import Point
import random
from flask import request, jsonify
from flask_restful import Resource, Api

from sqlalchemy.exc import IntegrityError

class TempApi(Resource):
    """ Dummy temperature api """
    def get(self):
        """ Generates random weekly maximum and minimum temp. value """
        days = ["Pzts", "Sali", "Cars", "Pers", "Cuma", "Cumrt", "Pazar"]
        return [{"minimum":random.randint(15, 25), "maximum":random.randint(25, 30), "day":day} for day in days]

class PointApi(Resource):
    """  """
    def get(self, point_name):
        """ """
        point = Point.query.filter_by(pointName=point_name).first()
        # basic model to json
        if point:
            json_point = {name:value for name, value in vars(point).items() if isinstance(value, (str, float, int))}
            return {'point':json_point}
        else:
            return {'point':None}

    def put(self, point_name):
        """ """
        try:
            if Point.query.filter_by(pointName=request.form['pointName']).first():
                point_query = Point.query.filter_by(pointName=request.form['pointName'])
                point_query.update({name:value for name, value in request.form.items()})
                db.session.commit()

                return self.serialize(point)
            else:
                point = Point(**{name:value for name, value in request.form.items()})
                db.session.add(p)
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
    api.add_resource(TempApi, "/api/temp/")
    api.add_resource(PointListApi, "/api/point/")
    api.add_resource(PointApi, '/api/point/<point_name>')
