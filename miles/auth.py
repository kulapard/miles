from functools import wraps

from flask import session, jsonify, request, current_app


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'card_number' not in session or session['card_number'] is None:
            return jsonify({"msg": "Unauthorized"}), 401
        return func(*args, **kwargs)

    return wrapper


def check_auth(username: str, password: str) -> bool:
    return username == current_app.config['LOGIN'] and password == current_app.config['PASSWORD']


def requires_basic_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return jsonify({"msg": "Unauthorized"}), 401
        return f(*args, **kwargs)

    return decorated
