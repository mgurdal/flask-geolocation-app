import os
from web_portal import app, db, Point
import unittest
import tempfile

class PointTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, app.config['DATABASE'] = tempfile.mkstemp()
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        app.config['TESTING'] = True

    def test_point_create(self):
        test_point = Point(pointName="tes1t", pointLatitude=0., pointLongitude=0.)

        db.session.add(test_point)
        db.session.commit()
        
        result = Point.query.filter_by(pointName='test1').first()
        self.assertIsNotNone(result)
        self.assertEquals(result.id, test_point.id)

    def test_point_update(self):
        test_point = Point(pointName="test2", pointLatitude=0., pointLongitude=0.)
        db.session.add(test_point)
        db.session.commit()
        db.session.rollback()

        point_query = Point.query.filter_by(pointName='test2')
        point_query.update({"pointLongitude":1.})
        db.session.commit()

        result = point_query.first()
        self.assertIsNotNone(result)
        self.assertEquals(result.pointLongitude, 1.)

    def test_point_removal(self):
        num_rows_deleted = db.session.query(Point).delete() 
        db.session.commit()
        db.session.rollback()
        self.assertEquals(2, num_rows_deleted)

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(app.config['DATABASE'])

if __name__ == '__main__':
    unittest.main()