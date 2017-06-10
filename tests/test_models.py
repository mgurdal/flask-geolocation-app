import os
from web_portal import app, db, Point
import unittest
import tempfile
import sys
class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, app.config['DATABASE'] = tempfile.mkstemp()
        sys.stderr.write(app.config['DATABASE'])
        app.config['TESTING'] = True
        self.app = app.test_client()

    def test_point_create(self):
        test_point = Point(pointName="test", pointLatitude=0., pointLongitude=0.)
        db.session.add(test_point)
        db.session.commit()
        result = Point.query.filter_by(pointName='test').first()
        self.assertIsNotNone(result)
        self.assertEquals(result.id, test_point.id)

    def test_point_update(self):
        test_point = Point(pointName="test", pointLatitude=0., pointLongitude=0.)
        db.session.add(test_point)
        db.session.commit()

        point_query = Point.query.filter_by(pointName='test')
        point_query.update({"pointLongitude":1.})
        db.session.commit()

        result = point_query.first()
        self.assertIsNotNone(result)
        self.assertEquals(result.pointLongitude, 1.)

    def test_point_removal(self):
        num_rows_deleted = db.session.query(Point).delete()
        db.session.commit()
        self.assertEquals(1, num_rows_deleted)

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(app.config['DATABASE'])

if __name__ == '__main__':
    unittest.main()