from functools import wraps
from flask import request
from app.models.models import User
from app.custom_http_respones.responses import Success, Error

success = Success()
error = Error()


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        access_token = None
        if 'Authorization' in request.headers:
            auth_header = request.headers.get('Authorization')
            access_token = auth_header.split(" ")[1]
        if not access_token:
            return error.unauthorized("Please login to perform this action")
        user_id = User.decode_token(access_token)
        if isinstance(user_id, str):
            return error.forbidden_action("Token has been rejected")
        return f(*args, user_id=user_id, **kwargs)
    return decorated


def admin_only(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        access_token = None
        if 'Authorization' in request.headers:
            auth_header = request.headers.get('Authorization')
            access_token = auth_header.split(" ")[1]
        if not access_token:
            return error.unauthorized("Please login to perform this action")
        user_id = User.decode_token(access_token)
        if isinstance(user_id, str):
            return error.forbidden_action("Token has been rejected")
        user = User.query.filter_by(id=user_id).first()
        if not user.admin:
            return error.unauthorized("This action can only be performed by admin")
        return f(*args, user_id=user_id, **kwargs)
    return decorated



