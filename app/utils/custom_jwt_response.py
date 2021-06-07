from functools import wraps
from flask import jsonify
try:
    from flask import _app_ctx_stack as ctx_stack
except ImportError:  # pragma: no cover
    from flask import _request_ctx_stack as ctx_stack
from flask_jwt_extended import jwt_required
from flask_jwt_extended.view_decorators import _decode_jwt_from_headers, verify_jwt_in_request
from flask_jwt_extended.exceptions import NoAuthorizationError, InvalidHeaderError

def protected():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            try:
                jwt_data = _decode_jwt_from_headers()
                ctx_stack.top.jwt = jwt_data
            except (NoAuthorizationError, InvalidHeaderError):
                print('invalid')
                return jsonify(msg="Unathorization"), 403
        return decorator

    return jwt_required(wrapper)