from flask import request, abort
from functools import wraps
from ..models import AuthApi
from ..default_settings import PROVIDER_SIGNATURE


def require_api_key(api_method):
    """
        this decorator protected invalid client access to backend
        based on client-secret and api-key

    :param api_method:
    :return:
    """
    @wraps(api_method)
    def check_api_key(*args, **kwargs):
        signature = request.headers.get('xf-provider-signature')

        if not signature or signature != PROVIDER_SIGNATURE:
            abort(401)

        client_secret = request.headers.get('xf-client-secret')
        api_key = request.headers.get('xf-api-key')

        if not client_secret and not api_key:
            abort(401)

        client = AuthApi.query.filter_by(client_secret=client_secret).first()
        if client is not None and client.api_key == api_key:
            return api_method(*args, **kwargs)
        else:
            abort(401)

    return check_api_key
