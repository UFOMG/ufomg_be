import datetime
import json
import bleach
from flask import request
from flask_restful import Resource, abort
from sqlalchemy.orm.exc import NoResultFound
from api import db
from api.database.models import Report

def _render_comments(comment_obj):
    comment_list = []
    for comment in comment_obj:
        comment_list.append(comment.text)
    return comment_list

def _validate_field(data, field, proceed, errors, missing_okay=False):
    if field in data:
        if type(data[field]) is str:
            data[field] = data[field].strip()
        if len(str(data[field])) == 0:
            proceed = False
            errors.append(f"required '{field}' parameter is blank")
    if not missing_okay and field not in data:
        proceed = False
        errors.append(f"required '{field}' parameter is missing")
        data[field] = ''
    return proceed, data[field], errors
def _reports_payload(report):
    return {
        'id': report.id,
        'name': report.name,
        'lat': report.lat,
        'long': report.long,
        'event_type': report.event_type,
        'description': report.description,
        'image': report.image,
        'city': report.city,
        'state': report.state,
        'links': {
            'get': f'/api/v1/reports/{report.id}',
            'delete': f'/api/v1/reports/{report.id}',
            'index': '/api/v1/reports'
        }
    }
def _report_payload(report):
    return {
        'id': report.id,
        'name': report.name,
        'lat': report.lat,
        'long': report.long,
        'event_type': report.event_type,
        'description': report.description,
        'image': report.image,
        'city': report.city,
        'state': report.state,
        'comments': _render_comments(report.comments),
        'links': {
            'get': f'/api/v1/reports/{report.id}',
            'delete': f'/api/v1/reports/{report.id}',
            'index': '/api/v1/reports'
        }
    }
class ReportsResource(Resource):
    def _create_report(self, data):
        proceed = True
        errors = []

        proceed, report_event_type, errors = _validate_field(
            data, 'event_type', proceed, errors)
        proceed, report_description, errors = _validate_field(
            data, 'description', proceed, errors)
        proceed, report_lat, errors = _validate_field(
            data, 'lat', proceed, errors)
        proceed, report_long, errors = _validate_field(
            data, 'long', proceed, errors)
        proceed, report_city, errors = _validate_field(
            data, 'city', proceed, errors)
        proceed, report_state, errors = _validate_field(
            data, 'state', proceed, errors)

        if proceed:
            report = Report(
                name=data['name'],
                lat=data['lat'],
                long=data['long'],
                event_type=data['event_type'],
                description=data['description'],
                image=data['image'],
                city=data['city'],
                state=data['state']
            )
            db.session.add(report)
            db.session.commit()
            return report, errors
        else:
            return None, errors
    def post(self, *args, **kwargs):
        report, errors = self._create_report(json.loads(request.data))
        if report is not None:
            report_payload = _report_payload(report)
            report_payload['success'] = True
            return report_payload, 201
        else:
            return {
                'success': False,
                'error': 400,
                'errors': errors
            }, 400
    def get(self, *args, **kwargs):
        reports = Report.query.order_by(
            Report.name.asc()
        ).all()
        results = [_reports_payload(report) for report in reports]
        return {
            'success': True,
            'results': results
        }, 200
class ReportResource(Resource):
    def get(self, *args, **kwargs):
        report_id = int(bleach.clean(kwargs['report_id'].strip()))
        report = None
        try:
            report = db.session.query(Report).filter_by(id=report_id).one()
        except NoResultFound:
            return abort(404)
        report_payload = _report_payload(report)
        report_payload['success'] = True
        return report_payload, 200
    def delete(self, *args, **kwargs):
        report_id = kwargs['report_id']
        report = None
        try:
            report = db.session.query(Report).filter_by(id=report_id).one()
        except NoResultFound:
            return abort(404)
        report.delete()
        return {}, 204
