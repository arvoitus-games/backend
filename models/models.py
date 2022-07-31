from datetime import datetime

from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

db = SQLAlchemy()


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


class Game(db.Model):
    """
    Game.
    """
    __tablename__ = 'game'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    comment = db.Column(db.String)


class Difficulty(db.Model):
    """
    Different difficulties for games.
    """
    __tablename__ = 'difficulty'
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String)


class GameRound(db.Model):
    """
    Description of Game Round.
    """
    __tablename__ = 'game_round'
    id = db.Column(db.Integer, primary_key=True)
    round_number = db.Column(db.Integer)
    difficulty_id = db.Column(db.Integer, ForeignKey('difficulty.id'))
    game_id = db.Column(db.Integer, ForeignKey("game.id"))

    difficulty = relationship('Difficulty')
    game = relationship("Game")


class GameRoundPlayer(db.Model):
    """
    User's result on the round.
    """
    __tablename__ = 'game_round_player'
    round_number = db.Column(db.Integer, ForeignKey("game_round.id"), primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey("user.id"), primary_key=True)

    passed_date = db.Column(db.DateTime(), default=datetime.utcnow, index=True)

    score = db.Column(db.Integer)

    round = relationship("GameRound", foreign_keys=[round_number])
    user = relationship("User", foreign_keys=[user_id])
