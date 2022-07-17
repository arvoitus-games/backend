import os
from datetime import datetime

from psycopg2.errors import UniqueViolation
from flask import Flask, flash, request, redirect, url_for, render_template, jsonify, abort
from sqlalchemy import ForeignKey
from sqlalchemy.exc import PendingRollbackError, IntegrityError
from sqlalchemy.orm import relationship
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash

from flask_login import LoginManager, login_required, login_user, logout_user
from flask_login import UserMixin, current_user
from flask_sqlalchemy import SQLAlchemy

from email_validator import validate_email, EmailNotValidError

login_manager = LoginManager()


app = Flask(__name__)
app.secret_key = 'super secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://root:example@localhost:5432'
login_manager.init_app(app)
db = SQLAlchemy(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


# move to sep class
# check creation table in database
class User(UserMixin, db.Model):
    """An admin user capable of viewing reports.

    :param str email: email address of user
    :param str password: encrypted password for the user

    """
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    authenticated = db.Column(db.Boolean, default=False)
    registration_date = db.Column(db.DateTime(), default=datetime.utcnow, index=True)

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.id

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False
####
#### end


class Game(db.Model):
    """

    """
    __tablename__ = 'game'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    comment = db.Column(db.String)


class Difficulty(db.Model):
    """
    Different difficulties for game
    """
    __tablename__ = 'difficulty'
    value = db.Column(db.String, primary_key=True)


class GameRound(db.Model):
    """
    Description of Game Round.
    """
    __tablename__ = 'game_round'
    id = db.Column(db.Integer, primary_key=True)
    round_number = db.Column(db.Integer)
    difficulty_value = db.Column(db.String, ForeignKey('difficulty.value'))
    game_id = db.Column(db.Integer, ForeignKey("game.id"))

    difficulty = relationship('Difficulty')
    game = relationship("Game")


class GameRoundPlayer(db.Model):
    """
    User's result on round
    """
    __tablename__ = 'game_round_player'
    round_number = db.Column(db.Integer, ForeignKey("game_round.id"), primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey("user.id"), primary_key=True)

    passed_date = db.Column(db.DateTime(), default=datetime.utcnow, index=True)

    score = db.Column(db.Integer)

    round = relationship("GameRound", foreign_keys=[round_number])
    user = relationship("User", foreign_keys=[user_id])


engine = db.create_engine('postgresql://root:example@localhost:5432', {})
with app.app_context():
    db.create_all(app=app)


def _register_user(email, password):
    try:
        validate_email(email)
    except EmailNotValidError:
        abort(jsonify(error='please use valid email'))
    hashed_password = generate_password_hash(password=password, method="pbkdf2:sha256")
    user = User(email=email, password=hashed_password)
    try:
        db.session.add(user)
        db.session.commit()
    except IntegrityError as error:
        if 'duplicate key' in error.orig.pgerror:
            abort(jsonify(error='this email already registered'))
        abort(jsonify('postgres_error'))
    return jsonify(success=True)


@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    email = request.args.get('email')
    password = request.args.get('password')
    if email and password:
        _register_user(email, password)
    return jsonify(success=False)


@login_manager.user_loader
def load_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    return user

##???
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField

class LoginForm(FlaskForm):
    username = StringField('Username')
    password = PasswordField('Password')
    submit = SubmitField('Submit')
##???

@app.route('/login')
def login():
    # if current_user.is_authenticated:
    #     pass

    form = LoginForm()
    args = request.args
    email = args.get('email')
    password = args.get('password')
    if email and password:
        user = User.query.filter_by(email=email, password=password).first()
        if user:
            login_user(user)
            flash('Logged in successfully.')
            return jsonify(success=True)
        return jsonify(success=False, error='wrong email or password')
    return jsonify(success=False, error='missing email or password')


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return jsonify(message='log out')

@app.route('/score')
@login_required
def score():
    user_id = request.args.get('user_id')
    player = GameRoundPlayer.query.filter_by(user_id=user_id).first()
    if player:
        return jsonify(player.score)
    return jsonify(error='No score yet or wrong user_id')


@app.route('/set_score')
@login_required
def set_score():
    round_id = request.args.get('round_id')
    score = request.args.get('score')
    user_id = request.args.get('user_id')

    player = GameRoundPlayer.query.filter_by(user_id=user_id).first()
    if player:
        return jsonify(player.score)
    return jsonify(error='No score yet or wrong user_id')

app.run()
