from flask import jsonify
from .models import User
from .util.library import current_timestamp_tz


def build_message_rest(name, message, status_code, issue=None, issue_message=None):
    """Build a JSON message for REST-API integration
    
    {
        "name": "AUTHENTICATION_REQUIRED_ERROR",
        "message": "Authentication Credentials is not valid",
        "status_code": 401,
        "timestamp": 1519932912012,
        "issues": [
            {
                "issue": "InsufficientAuthenticationException",
                "message": "Full authentication is required to access this resource"
            }
        ]
    }
    """

    # wrap = {'success': success, 'status_code': status_code, 'message': message}
    wrap = {'name': name,
            'message': message,
            'status_code': status_code,
            'timestamp': current_timestamp_tz(),
            'issues': [{
                "issue": issue,
                "message": issue_message
            }]}

    return jsonify(wrap)


class BaseObjectAPI(object):
    def __init__(self, data_as_json):
        self.errors = []
        self.data_as_json = data_as_json

    def validate_required_fields(self, field):
        if not self.data_as_json.get(field):
            self.errors.append('{} field is required'.format(field))

    def get_message_errors(self):
        message = []
        for e in self.errors:
            message.append(e)
        return message


class UserAPI(BaseObjectAPI):
    def user_check_unique(self, field):
        if field == 'email':
            r_query = User.query.filter_by(user_email=self.data_as_json.get('user_email'))

        internal = self.data_as_json.get('internal')
        if internal:
            r_query = r_query.filter(User.internal != internal)

        if r_query.first():
            self.errors.append(u'E-mail informado já encontra-se cadastrado.')
