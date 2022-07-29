from email_validator import validate_email, EmailNotValidError
from flask import jsonify
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import abort
from werkzeug.security import generate_password_hash

from models.models import User, db


def _generate_password_hash(password):
    return generate_password_hash(password=password, method="pbkdf2:sha256")


def _register_user(email, password):
    try:
        validate_email(email)
    except EmailNotValidError:
        abort(jsonify(error='please use valid email'))
    hashed_password = _generate_password_hash(password)
    user = User(email=email, password=hashed_password)
    try:
        db.session.add(user)
        db.session.commit()
    except IntegrityError as error:
        if 'duplicate key' in error.orig.pgerror:
            abort(jsonify(error='this email already registered'))
        abort(jsonify('postgres_error'))
    return jsonify(success=True)
