
import os
import unittest
from flask import json

from main import app, db, Point


class PointApiTestCase(unittest.TestCase):

    def setUp(self):
        app.config.from_pyfile('test_config.py')
        self.test_point = Point(pointName="test", pointLatitude=0., pointLongitude=0.)
        db.create_all()

        db.session.add(self.test_point)
        db.session.commit()
        self.client = app.test_client()

    def test_get_all_points(self):
        response = self.client.get('/api/point', follow_redirects=True)
        response_data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response_data, dict)
        self.assertIn('point', response_data.keys())
        self.assertEquals(len(response_data['point']), 1)
        self.assertEquals(response_data['point'][0]['pointName'], 'test')

    def test_get_point_by_name(self):
        response = self.client.get('/api/point/test', follow_redirects=True)
        response_data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response_data, dict)
        self.assertIn('point', response_data.keys())
        self.assertEquals(len(response_data['point']), 4)
        self.assertEquals(response_data['point']['pointName'], 'test')
        self.assertEquals(response_data['point']['pointLatitude'], 0.)
        self.assertEquals(response_data['point']['pointLongitude'], 0.)

    def test_add_point_by_name(self):
        data = {'pointName':'add_test', 'pointLatitude':1., 'pointLongitude':1.}
        response = self.client.post('/api/point/new_point', data=data)
        response_data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response_data, dict)
        self.assertEquals(len(response_data), 4)
        self.assertEquals(response_data['pointName'], 'add_test')

    def test_delete_point_by_name(self):
        data = {'pointName':'test', 'pointLatitude':1., 'pointLongitude':1.}
        response = self.client.post('/api/point/new_point', data=data)

        response = self.client.delete('/api/point/test')
        response_data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response_data, dict)
        self.assertEquals(response_data['status'], 'success')

    def tearDown(self):
        db.session.remove()
        db.drop_all()

class TempApiTestCase(unittest.TestCase):
    
    def setUp(self):
        app.config.from_pyfile('test_config.py')
        self.test_point = Point(pointName="test", pointLatitude=0., pointLongitude=0.)
        db.create_all()

        db.session.add(self.test_point)
        db.session.commit()
        self.client = app.test_client()

    def test_get_location_daily_temp_info(self):
        data = {'points[0][pointLatitude]': ['0.0'],
                'points[0][pointLongitude]': ['0.0'],
                'points[0][pointName]': ['test']}

        response = self.client.post('/api/temp', data=data)
        response_data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response_data, list)
        self.assertEquals(len(response_data), 1)
        temp_data = response_data[0]
        self.assertIn('label', temp_data)
        self.assertIn('data', temp_data)
        self.assertIsInstance(temp_data['data'][0], dict)
        self.assertListEqual(sorted(list(temp_data['data'][0].keys())), ['day', 'maximum', 'minimum'])

    def tearDown(self):
        db.session.remove()
        db.drop_all()