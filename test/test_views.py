import sys
import os
from main import app, db, Point
import unittest
import tempfile

class IndexTestCase(unittest.TestCase):

    def setUp(self):
        app.config.from_pyfile('test_config.py')
        self.test_point = Point(pointName="test", pointLatitude=0., pointLongitude=0.)
        db.create_all()
        self.client = app.test_client()

    def test_get_index(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<title>Flask Geolocation App</title>', response.data)
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()
