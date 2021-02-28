import unittest
from sqlalchemy.exc import IntegrityError

from api import create_app, db
from api.database.models import Report, Comment


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

    def test_comment_model(self):
        report = Report(name='Mark Zuckerberg', lat=3.123, long=3.345, city='Roswell', state='NM',
                        description="I am your reptilian overloard!", event_type="encounter", image="pics.com")
        comment = Comment(text='I knew it!', report_id={report.id})
        report.comments.append(comment)
        db.session.add(report)
        db.session.commit()

        self.assertIsInstance(comment, Comment)
        self.assertIsNotNone(comment.id)
        self.assertEqual('I knew it!', comment.text)
        self.assertEqual(report.id, comment.report_id)

    def test_report_model_with_forced_id(self):
        report = Report(name='Mark Zuckerberg', lat=3.123, long=3.345, city='Roswell', state='NM',
                        description="I am your reptilian overloard!", event_type="encounter", image="pics.com", report_id=1)
        comment = Comment(text='I knew it!', report_id=1)
        report.comments.append(comment)
        db.session.add(report)
        db.session.commit()

        self.assertIsInstance(comment, Comment)
        self.assertIsNotNone(comment.id)
        self.assertEqual(1, comment.id)
        self.assertEqual('I knew it!', comment.text)

    # def test_report_model_missing_text(self):
    #     try:
    #         report = Report(name='Mark Zuckerberg', lat=3.123, long=3.345, city='Roswell', state='NM',
    #                         description="I am your reptilian overloard!", event_type="encounter", image="pics.com")
    #         comment = Comment(report_id={report.id})
    #         report.comments.append(comment)
    #         db.session.add(report)
    #         db.session.commit()
    #     except IntegrityError:
    #         self.assertTrue(True)
    #     else:
    #         # we should not end up in here
    #         self.assertTrue(False)  # pragma: no cover

    def test_report_model_blank_text(self):
        try:
            report = Report(name='Mark Zuckerberg', lat=3.123, long=3.345, city='Roswell', state='NM',
                            description="I am your reptilian overloard!", event_type="encounter", image="pics.com")
            comment = Comment(text='', report_id={report.id})
            report.comments.append(comment)
            db.session.add(report)
            db.session.commit()
        except IntegrityError:
            self.assertTrue(True)
        else:
            # we should not end up in here
            self.assertTrue(False)  # pragma: no cover

    # def test_report_model_missing_report_id(self):
    #     try:
    #         report = Report(name='Mark Zuckerberg', lat=3.123, long=3.345, city='Roswell', state='NM',
    #                         description="I am your reptilian overloard!", event_type="encounter", image="pics.com")
    #         comment = Comment(text='I knew it!', report_id='')
    #         report.comments.append(comment)
    #         db.session.add(report)
    #         db.session.commit()
    #     except IntegrityError:
    #         self.assertTrue(True)
    #     else:
    #         # we should not end up in here
    #         self.assertTrue(False)  # pragma: no cover

    # def test_report_model_blank_report_id(self):
    #     try:
    #         report = Report(name='Mark Zuckerberg', lat=3.123, long=3.345, city='Roswell', state='NM',
    #                         description="I am your reptilian overloard!", event_type="encounter", image="pics.com")
    #         comment = Comment(text='I knew it!', report_id=None)
    #         report.comments.append(comment)
    #         db.session.add(report)
    #         db.session.commit()
    #     except IntegrityError:
    #         self.assertTrue(True)
    #     else:
    #         # we should not end up in here
    #         self.assertTrue(False)  # pragma: no cover
