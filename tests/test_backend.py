
import os
import tempfile
import unittest

from web_portal.main import app, api

class FlaskTestCase(unittest.TestCase):
    
    def setUp(self):
        self.db_fd, app.config['DATABASE'] = tempfile.mkstemp()
        self.app = app.test_client()
        api.add_resource(PointApi, '/api/point/<point_name>')
    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(flaskr.app.config['DATABASE'])

    def test_empty_db(self):
        rv = self.app.get('/')
        assert b'No entries here so far' in rv.data