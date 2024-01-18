from flask import jsonify
from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt


def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt()
        if claims['role'] == 0:
            return func(*args, **kwargs)
        else:
            return jsonify(
                msg='Admin only.'
            ), 403
    return wrapper
