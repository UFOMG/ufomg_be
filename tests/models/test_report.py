import unittest
from sqlalchemy.exc import IntegrityError

from api import create_app, db
from api.database.models import Report


class AppTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_report_model(self):
        report = Report(name='Mark Zuckerberg', lat=3.123, long=3.345, city='Roswell', state='NM',
                        description="I am your reptilian overloard!", event_type="encounter", image="pics.com")
        report.insert()

        self.assertIsInstance(report, Report)
        self.assertIsNotNone(report.id)
        self.assertEqual('Mark Zuckerberg', report.name)
        self.assertEqual(3.123, report.lat)
        self.assertEqual(3.345, report.long)
        self.assertEqual("I am your reptilian overloard!", report.description)
        self.assertEqual("encounter", report.event_type)
        self.assertEqual("pics.com", report.image)

    def test_report_model_with_forced_id(self):
        report = Report(name='Mark Zuckerberg', lat=3.123123, long=3.345345, city='Roswell', state='NM',
                        description="I am your reptilian overloard!", event_type="encounter", image="pics.com", report_id=1)
        report.insert()

        self.assertIsInstance(report, Report)
        self.assertIsNotNone(report.id)
        self.assertEqual(1, report.id)
        self.assertEqual('Mark Zuckerberg', report.name)
        self.assertEqual(3.123, report.lat)
        self.assertEqual(3.345, report.long)
        self.assertEqual("I am your reptilian overloard!", report.description)
        self.assertEqual("encounter", report.event_type)
        self.assertEqual("pics.com", report.image)

    def test_report_model_blank_name_will_be_stored_as_anonymous(self):
        try:
            report = Report(name='', lat=3.123123, long=3.345345, city='Roswell', state='NM',
                            description="I am your reptilian overloard!", event_type="encounter", image="pics.com")
            report.insert()
            db.session.query(Report).filter_by(name='anonymous').first()
        except IntegrityError:
            self.assertTrue(False)
        else:
            # we should not end up in here
            self.assertTrue(True)  # pragma: no cover

    # def test_report_model_missing_name_will_be_stored_as_anonymous(self):
    #     try:
    #         report = Report(name=None, lat=3.123123, long=3.345345, description="I am your reptilian overloard!", event_type="encounter", image="pics.com")
    #         report.insert()
    #         db.session.query(Report).filter_by(name='anonymous').first()
    #     except IntegrityError:
    #         self.assertTrue(True)
    #     else:
    #         # we should not end up in here
    #         self.assertTrue(False)  # pragma: no cover

    # def test_report_model_missing_latitude(self):
    #     try:
    #         report = Report(name='Mark Zuckerberg', lat=None, long=3.345345, description="I am your reptilian overloard!", event_type="encounter", image="pics.com")
    #         report.insert()
    #     except IntegrityError:
    #         self.assertTrue(True)
    #     else:
    #         # we should not end up in here
    #         self.assertTrue(False)  # pragma: no cover

    # def test_report_model_missing_longitude(self):
    #     try:
    #         report = Report(name='Mark Zuckerberg', lat=3.123123, long=None, description="I am your reptilian overloard!", event_type="encounter", image="pics.com")
    #         report.insert()
    #     except IntegrityError:
    #         self.assertTrue(True)
    #     else:
    #         # we should not end up in here
    #         self.assertTrue(False)  # pragma: no cover

    # def test_report_model_blank_description(self):
    #     try:
    #         report = Report(name='', lat=3.123123, long=3.345345, description="", event_type="encounter", image="pics.com")
    #         report.insert()
    #     except IntegrityError:
    #         self.assertTrue(False)
    #     else:
    #         # we should not end up in here
    #         self.assertTrue(True)  # pragma: no cover

    def test_report_model_missing_description(self):
        try:
            report = Report(name=None, lat=3.123123, long=3.345345,
                            description=None, event_type="encounter", image="pics.com")
            report.insert()
        except IntegrityError:
            self.assertTrue(True)
        else:
            # we should not end up in here
            self.assertTrue(False)  # pragma: no cover

    # def test_report_model_blank_event_type(self):
    #     try:
    #         report = Report(name='', lat=3.123123, long=3.345345, description="I am your reptilian overloard!", event_type="", image="pics.com")
    #         report.insert()
    #         session.query(report).filter(name='anonymous').one()
    #     except IntegrityError:
    #         self.assertTrue(False)
    #     else:
    #         # we should not end up in here
    #         self.assertTrue(True)  # pragma: no cover

    def test_report_model_missing_description(self):
        try:
            report = Report(name=None, lat=3.123123, long=3.345345, city='Roswell', state='NM',
                            description="I am your reptilian overloard!", event_type=None, image="pics.com")
            report.insert()
        except IntegrityError:
            self.assertTrue(True)
        else:
            # we should not end up in here
            self.assertTrue(False)  # pragma: no cover
