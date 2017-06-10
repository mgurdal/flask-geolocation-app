import os

import unittest
from main import app, db, Point

class PointTestCase(unittest.TestCase):

    def setUp(self):
        
        app.config.from_pyfile('test_config.py')
        self.test_point = Point(pointName="test", pointLatitude=0., pointLongitude=0.)
        db.create_all()

    def test_point_create(self):
        
        db.session.add(self.test_point)
        db.session.commit()
        
        result = Point.query.filter_by(pointName='test').first()
        self.assertIsNotNone(result)
        self.assertEquals(result.id, self.test_point.id)

    def test_point_update(self):
        db.session.add(self.test_point)
        db.session.commit()

        point_query = self.test_point.query.filter_by(pointName='test')
        point_query.update({"pointLongitude":1.})
        db.session.commit()

        result = self.test_point.query.first()
        self.assertIsNotNone(result)
        self.assertEquals(result.pointLongitude, 1.)

    def test_point_removal(self):
        db.session.add(self.test_point)
        db.session.commit()

        num_rows_deleted = db.session.query(Point).delete() 
        db.session.commit()
        
        self.assertEquals(num_rows_deleted, 1, )

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        #os.remove('test.db')
if __name__ == '__main__':

    unittest.main()