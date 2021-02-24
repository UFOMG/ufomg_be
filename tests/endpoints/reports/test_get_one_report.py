import json
import unittest
from unittest.mock import patch

from api import create_app, db
from api.database.models import Report
from tests import db_drop_everything, assert_payload_field_type_value, \
    assert_payload_field_type


class GetReportTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

        self.report_1 = Report(name='Mark Zuckerberg', lat=3.123, long=3.345345, city='Roswell', state='NM',
                               description="I am your reptilian overloard!", event_type="encounter", image="pics.com")
        self.report_1.insert()

    def tearDown(self):
        db.session.remove()
        db_drop_everything(db)
        self.app_context.pop()

    def test_happypath_get_a_report(self):
        response = self.client.get(
            f'/api/v1/reports/{self.report_1.id}'
        )
        self.assertEqual(200, response.status_code)

        data = json.loads(response.data.decode('utf-8'))
        assert_payload_field_type_value(self, data, 'success', bool, True)

        assert_payload_field_type_value(
            self, data, 'name', str, self.report_1.name
        )
        assert_payload_field_type_value(
            self, data, 'lat', float, self.report_1.lat
        )
        assert_payload_field_type_value(
            self, data, 'long', float, self.report_1.long
        )
        assert_payload_field_type_value(
            self, data, 'description', str, self.report_1.description
        )
        assert_payload_field_type_value(
            self, data, 'event_type', str, self.report_1.event_type
        )
        assert_payload_field_type_value(
            self, data, 'image', str, self.report_1.image
        )

        report_id = data['id']
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

    def test_endpoint_sadpath_bad_id_report(self):
        response = self.client.get(
            f'/api/v1/reports/9999'
        )
        self.assertEqual(404, response.status_code)

        data = json.loads(response.data.decode('utf-8'))
        assert_payload_field_type_value(self, data, 'error', int, 404)
        assert_payload_field_type_value(self, data, 'success', bool, False)
        assert_payload_field_type_value(
            self, data, 'message', str, 'resource not found'
        )
