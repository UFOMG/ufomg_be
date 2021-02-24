import datetime
import json
import bleach
from flask import request
from flask_restful import Resource, abort
from sqlalchemy.orm.exc import NoResultFound
from api import db
from api.database.models import Comment

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
def _comment_payload(comment):
    return {
        'text': comment.text,
        'report_id': comment.report_id
    }
class CommentsResource(Resource):
    def _create_comment(self, data):
        proceed = True
        errors = []

        proceed, text, errors = _validate_field(
            data, 'text', proceed, errors)

        if proceed:
            comment = Comment(
                text=data['text'],
                report_id=data['report_id']
            )
            import pdb; pdb.set_trace()
            db.session.add(comment)
            db.session.commit()
            return comment, errors
        else:
            return None, errors
    def post(self, *args, **kwargs):
        comment, errors = self._create_comment(json.loads(request.data))
        if comment is not None:
            comment_payload = _comment_payload(comment)
            comment_payload['success'] = True
            return comment_payload, 201
        else:
            return {
                'success': False,
                'error': 400,
                'errors': errors
            }, 400
