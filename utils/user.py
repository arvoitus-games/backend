from email_validator import validate_email, EmailNotValidError
from flask import jsonify, url_for
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import abort
from werkzeug.security import generate_password_hash

from models.models import User, db

from confirmation import generate_confirmation_token, confirm_token

def generate_password_hash_sha256(password):
    return generate_password_hash(password=password, method="pbkdf2:sha256")


def register_user(email, password, name):
    _register_user(email, password, name)


def _register_user(email, password, name):
    try:
        validate_email(email)
    except EmailNotValidError:
        abort(jsonify(error="please use valid email"))
    hashed_password = generate_password_hash_sha256(password)
    if name is None: name = "Player"
    user = User(email=email, password=hashed_password, name=name, confirmed=False)

    token = generate_confirmation_token(user.email)
    confirm_url = url_for('confirm_email', token=token, _external=True)
    send_confirmation_email(email, name, confirm_url)

    try:
        db.session.add(user)
        db.session.commit()
    except IntegrityError as error:
        if "duplicate key" in error.orig.pgerror:
            abort(jsonify(error="this email already registered"))
        abort(jsonify("postgres_error"))
    return jsonify(success=True, id=str(user.id))
