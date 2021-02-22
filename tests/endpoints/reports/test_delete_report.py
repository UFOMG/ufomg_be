import json
import unittest
from unittest.mock import patch

from api import create_app, db
from api.database.models import Report
from tests import db_drop_everything, assert_payload_field_type_value


class DeleteReportTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

        self.report_1 = Report(name='Phil', lat=3.123123, long=3.345345, description="some crazy stuff happened", event_type="abduction", image="image.com")
        self.report_1.insert()

    def tearDown(self):
        db.session.remove()
        db_drop_everything(db)
        self.app_context.pop()

    def test_happypath_delete_a_report(self):
        response = self.client.delete(
            f'/api/v1/reports/{self.report_1.id}'
        )
        self.assertEqual(204, response.status_code)
        self.assertEqual('', response.data.decode('utf-8'))

        # ensure it's really gone by getting a 404 if we try to fetch it again
        response = self.client.get(
            f'/api/v1/reports/{self.report_1.id}'
        )
        self.assertEqual(404, response.status_code)

    def test_sadpath_delete_bad_id_report(self):
        response = self.client.delete(
            f'/api/v1/reports/9999999'
        )
        self.assertEqual(404, response.status_code)

        data = json.loads(response.data.decode('utf-8'))
        assert_payload_field_type_value(self, data, 'error', int, 404)
        assert_payload_field_type_value(self, data, 'success', bool, False)
        assert_payload_field_type_value(
            self, data, 'message', str, 'resource not found'
        )
