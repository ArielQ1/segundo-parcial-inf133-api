from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from functools import wraps
from flask_login import current_user

def jwt_required(fn):
    @wraps(fn)
    def wrapper(*args, **kgars):
        try:
            verify_jwt_in_request()
            return fn(*args, **kgars)
        except Exception as e:
            return jsonify({"error": str(e)}), 401
    return wrapper

def role_required(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated or not current_user.has_role(role):
                jsonify({"error":"No tienes permisos para acceder a esta página."})
            return f(*args, **kwargs)

        return decorated_function

    return decorator