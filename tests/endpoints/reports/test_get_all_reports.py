import json
import unittest

from api import create_app, db
from api.database.models import Report
from tests import db_drop_everything, assert_payload_field_type_value, \
    assert_payload_field_type


class GetReportsTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db_drop_everything(db)
        self.app_context.pop()


class GetAllReportsTest(GetReportsTest):
    def test_happypath_get_all_reports(self):
        report_1 = Report(name='Will Smith', lat=3.123123, long=3.345345, city='Roswell', state='NM',
                          description="Halle Berry was an alien the whole time", event_type="encounter", image="pics.com")
        report_1.insert()
        report_2 = Report(name='Mark Zuckerberg', lat=3.123123, long=3.345345, city='Roswell', state='NM',
                          description="I am your reptilian overloard!", event_type="encounter", image="pics.com")
        report_2.insert()

        response = self.client.get(
            f'/api/v1/reports'
        )
        self.assertEqual(200, response.status_code)

        data = json.loads(response.data.decode('utf-8'))
        assert_payload_field_type_value(self, data, 'success', bool, True)
        assert_payload_field_type(self, data, 'results', list)

        results = data['results']

        # we expect report 2 first to ensure we're getting results in
        # ascending alphabetical order by name
        next_result = results[0]
        assert_payload_field_type_value(
            self, next_result, 'name', str, report_2.name
        )
        assert_payload_field_type_value(
            self, next_result, 'lat', float, report_2.lat
        )
        assert_payload_field_type_value(
            self, next_result, 'long', float, report_2.long
        )
        assert_payload_field_type_value(
            self, next_result, 'description', str, report_2.description
        )
        assert_payload_field_type_value(
            self, next_result, 'event_type', str, report_2.event_type
        )
        assert_payload_field_type_value(
            self, next_result, 'image', str, report_2.image
        )
        report_id = next_result['id']

        assert_payload_field_type(self, next_result, 'links', dict)

        links = next_result['links']
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

        next_result = results[1]
        assert_payload_field_type_value(
            self, next_result, 'name', str, report_1.name
        )
        assert_payload_field_type_value(
            self, next_result, 'lat', float, report_1.lat
        )
        assert_payload_field_type_value(
            self, next_result, 'lat', float, report_1.lat
        )
        assert_payload_field_type_value(
            self, next_result, 'event_type', str, report_1.event_type
        )
        assert_payload_field_type_value(
            self, next_result, 'description', str, report_1.description
        )
        assert_payload_field_type_value(
            self, next_result, 'image', str, report_1.image
        )
        report_id = next_result['id']

        assert_payload_field_type(self, next_result, 'links', dict)

    def test_happypath_get_empty_reports(self):
        response = self.client.get(
            f'/api/v1/reports'
        )
        self.assertEqual(200, response.status_code)

        data = json.loads(response.data.decode('utf-8'))
        assert_payload_field_type_value(self, data, 'success', bool, True)
        assert_payload_field_type(self, data, 'results', list)
        # results list should be empty
        self.assertEqual(0, len(data['results']))
