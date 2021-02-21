import datetime
import json

import bleach
from flask import request
from flask_restful import Resource, abort
from sqlalchemy.orm.exc import NoResultFound

from api import db
from api.database.models import Report


def _validate_field(data, field, proceed, errors, missing_okay=False):
    if field in data:
        # sanitize the report input here
        data[field] = bleach.clean(data[field].strip())
        if len(data[field]) == 0:
            proceed = False
            errors.append(f"required '{field}' parameter is blank")
    if not missing_okay and field not in data:
        proceed = False
        errors.append(f"required '{field}' parameter is missing")
        data[field] = ''

    return proceed, data[field], errors


def _report_payload(report):
    return {
        'id': report.id,
        'name': report.name,
        'lat': report.lat,
        'long': report.long,
        'links': {
            'get': f'/api/v1/reports/{report.id}',
            'patch': f'/api/v1/reports/{report.id}',
            'delete': f'/api/v1/reports/{report.id}',
            'index': '/api/v1/reports',
        }
    }


class ReportsResource(Resource):
    def _create_report(self, data):
        proceed = True
        errors = []

        if proceed:
            report = Report(
                name=name,
                description=description,
                lat=lat,
                long=long,
                event_type=event_type,
                image=image
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
            Report.id.asc()
        ).all()
        results = [_report_payload(report) for report in reports]
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

    def patch(self, *args, **kwargs):
        report_id = int(bleach.clean(kwargs['report_id'].strip()))
        report = None
        try:
            report = db.session.query(Report).filter_by(id=report_id).one()
        except NoResultFound:
            return abort(404)

        proceed = True
        errors = []
        data = json.loads(request.data)
        proceed, name, errors = _validate_field(
            data, 'name', proceed, errors, missing_okay=True)

        if not proceed:
            return {
                'success': False,
                'error': 400,
                'errors': errors
            }, 400

        if name and len(name.strip()) > 0:
            report.name = name
        report.update()

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
