import json
import unittest
from copy import deepcopy

from api import create_app, db
from tests import db_drop_everything, assert_payload_field_type_value, \
    assert_payload_field_type


class CreateReportTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

        # adding extra padding in here to ensure we strip() it off later
        self.payload = {
            'name': ' alien_lover ',
            'lat': 33.39,
            'long': 45.45,
            'description': 'They had really cute buggey eyes :D',
            'event_type': 'abduction',
            'image': 'image.jpg',
        }

    def tearDown(self):
        db.session.remove()
        db_drop_everything(db)
        self.app_context.pop()

    def test_happypath_create_report(self):
        payload = deepcopy(self.payload)

        response = self.client.post(
            '/api/v1/reports', json=payload,
            content_type='application/json'
        )
        self.assertEqual(201, response.status_code)

        data = json.loads(response.data.decode('utf-8'))
        assert_payload_field_type_value(self, data, 'success', bool, True)

        assert_payload_field_type(self, data, 'id', int)
        report_id = data['id']
        assert_payload_field_type_value(
            self, data, 'name', str, payload['name'].strip()
        )
        assert_payload_field_type_value(
            self, data, 'lat', float, payload['lat']
        )
        assert_payload_field_type_value(
            self, data, 'long', float, payload['long']
        )
        assert_payload_field_type_value(
            self, data, 'description', str, payload['description'].strip()
        )
        assert_payload_field_type_value(
            self, data, 'event_type', str, payload['event_type'].strip()
        )
        assert_payload_field_type_value(
            self, data, 'image', str, payload['image'].strip()
        )

        assert_payload_field_type(self, data, 'links', dict)
        links = data['links']
        assert_payload_field_type_value(
            self, links, 'get', str, f'/api/v1/reports/{report_id}'
        )
        assert_payload_field_type_value(
            self, links, 'patch', str, f'/api/v1/reports/{report_id}'
        )
        assert_payload_field_type_value(
            self, links, 'delete', str, f'/api/v1/reports/{report_id}'
        )
        assert_payload_field_type_value(
            self, links, 'index', str, '/api/v1/reports'
        )

    def test_happypath_blank_name(self):
        payload = deepcopy(self.payload)
        payload['name'] = ''
        response = self.client.post(
            '/api/v1/reports', json=payload,
            content_type='application/json'
        )
        self.assertEqual(201, response.status_code)

        data = json.loads(response.data.decode('utf-8'))
        assert_payload_field_type_value(self, data, 'success', bool, True)

    # def test_happypath_missing_name(self):
    #     payload = deepcopy(self.payload)
    #     del payload['name']
    #     response = self.client.post(
    #         '/api/v1/reports', json=payload,
    #         content_type='application/json'
    #     )
    #     self.assertEqual(201, response.status_code)

    #     data = json.loads(response.data.decode('utf-8'))
    #     assert_payload_field_type_value(self, data, 'success', bool, False)

    def test_happypath_blank_image(self):
        payload = deepcopy(self.payload)
        payload['image'] = ''
        response = self.client.post(
            '/api/v1/reports', json=payload,
            content_type='application/json'
        )
        self.assertEqual(201, response.status_code)

        data = json.loads(response.data.decode('utf-8'))
        assert_payload_field_type_value(self, data, 'success', bool, True)

    # def test_happypath_missing_image(self):
    #     payload = deepcopy(self.payload)
    #     del payload['image']
    #     response = self.client.post(
    #         '/api/v1/reports', json=payload,
    #         content_type='application/json'
    #     )
    #     self.assertEqual(201, response.status_code)

    #     data = json.loads(response.data.decode('utf-8'))
    #     assert_payload_field_type_value(self, data, 'success', bool, False)

    def test_sadpath_blank_latitude(self):
        payload = deepcopy(self.payload)
        payload['lat'] = ''
        response = self.client.post(
            '/api/v1/reports', json=payload,
            content_type='application/json'
        )
        self.assertEqual(201, response.status_code)

        data = json.loads(response.data.decode('utf-8'))
        assert_payload_field_type_value(self, data, 'success', bool, True)

    # def test_sadpath_missing_latitude(self):
    #     payload = deepcopy(self.payload)
    #     del payload['lat']
    #     response = self.client.post(
    #         '/api/v1/reports', json=payload,
    #         content_type='application/json'
    #     )
    #     self.assertEqual(400, response.status_code)

    #     data = json.loads(response.data.decode('utf-8'))
    #     assert_payload_field_type_value(self, data, 'success', bool, False)
    #     assert_payload_field_type_value(self, data, 'error', int, 400)
    #     assert_payload_field_type_value(
    #         self, data, 'errors', list,
    #         ["required 'latitude' parameter is missing"]
    #     )

    def test_sadpath_missing_longitude(self):
        payload = deepcopy(self.payload)
        del payload['long']
        response = self.client.post(
            '/api/v1/reports', json=payload,
            content_type='application/json'
        )
        self.assertEqual(400, response.status_code)

        data = json.loads(response.data.decode('utf-8'))
        assert_payload_field_type_value(self, data, 'success', bool, False)
        assert_payload_field_type_value(self, data, 'error', int, 400)
        assert_payload_field_type_value(
            self, data, 'errors', list,
            ["required 'longitude' parameter is missing"]
        )

    # def test_sadpath_blank_longitude(self):
    #     payload = deepcopy(self.payload)
    #     payload['long'] = ''
    #     response = self.client.post(
    #         '/api/v1/reports', json=payload,
    #         content_type='application/json'
    #     )
    #     self.assertEqual(201, response.status_code)

    #     data = json.loads(response.data.decode('utf-8'))
    #     assert_payload_field_type_value(self, data, 'success', bool, True)

    def test_sadpath_missing_description(self):
        payload = deepcopy(self.payload)
        del payload['description']
        response = self.client.post(
            '/api/v1/reports', json=payload,
            content_type='application/json'
        )
        self.assertEqual(400, response.status_code)

        data = json.loads(response.data.decode('utf-8'))
        assert_payload_field_type_value(self, data, 'success', bool, False)
        assert_payload_field_type_value(self, data, 'error', int, 400)
        assert_payload_field_type_value(
            self, data, 'errors', list,
            ["required 'description' parameter is missing"]
        )
    
    def test_sadpath_blank_description(self):
        payload = deepcopy(self.payload)
        payload['description'] = ''
        response = self.client.post(
            '/api/v1/reports', json=payload,
            content_type='application/json'
        )
        self.assertEqual(201, response.status_code)

        data = json.loads(response.data.decode('utf-8'))
        assert_payload_field_type_value(self, data, 'success', bool, True)

    def test_sadpath_blank_description(self):
        payload = deepcopy(self.payload)
        payload['description'] = ''
        response = self.client.post(
            '/api/v1/reports', json=payload,
            content_type='application/json'
        )
        self.assertEqual(400, response.status_code)

        data = json.loads(response.data.decode('utf-8'))
        assert_payload_field_type_value(self, data, 'success', bool, False)
        assert_payload_field_type_value(self, data, 'error', int, 400)
        assert_payload_field_type_value(
            self, data, 'errors', list,
            ["required 'description' parameter is blank"]
        )

    def test_sadpath_missing_event_type(self):
        payload = deepcopy(self.payload)
        del payload['event_type']
        response = self.client.post(
            '/api/v1/reports', json=payload,
            content_type='application/json'
        )
        self.assertEqual(400, response.status_code)

        data = json.loads(response.data.decode('utf-8'))
        assert_payload_field_type_value(self, data, 'success', bool, False)
        assert_payload_field_type_value(self, data, 'error', int, 400)
        assert_payload_field_type_value(
            self, data, 'errors', list,
            ["required 'event_type' parameter is missing"]
        )

    def test_sadpath_blank_event_type(self):
        payload = deepcopy(self.payload)
        payload['event_type'] = ' '
        response = self.client.post(
            '/api/v1/reports', json=payload,
            content_type='application/json'
        )
        self.assertEqual(400, response.status_code)

        data = json.loads(response.data.decode('utf-8'))
        assert_payload_field_type_value(self, data, 'success', bool, False)
        assert_payload_field_type_value(self, data, 'error', int, 400)
        assert_payload_field_type_value(
            self, data, 'errors', list,
            ["required 'event_type' parameter is blank"]
        )
