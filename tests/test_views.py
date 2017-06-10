import os
from web_portal import app, db, Point
import unittest
import tempfile

class IndexTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, app.config['DATABASE'] = tempfile.mkstemp()
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_get_index(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        