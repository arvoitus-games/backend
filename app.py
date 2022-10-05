import os
from datetime import datetime

from flask import Flask, request, jsonify, flash
from flask_login import (
    LoginManager,
    current_user,
    login_user,
    login_required,
    logout_user,
)
from flask_migrate import Migrate
from werkzeug.security import check_password_hash

from models.models import db, User, GameRoundPlayer, Difficulty, Game, GameRound

# from resource_classes import api
from utils.user import _register_user
from vars import POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_PORT


app = Flask(__name__)
app.secret_key = "super secret"
#uri = os.environ.get("URI")
uri = "postgresql+psycopg2://vkdgszieqyytdr:f8dd7698baa9c71efa566f30951c2e65226f90322989c3e37660a71adaa07af7@ec2-54-86-106-48.compute-1.amazonaws.com:5432/d8jqusjfu5ckah?sslmode=require"

login_manager = LoginManager()

# ns = api.namespace('user', description='User operations')
# ns_login = api.namespace('login', description='Auth')

if uri:
    app.config["SQLALCHEMY_DATABASE_URI"] = uri
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://root:example@localhost:5432"
login_manager.init_app(app)
db.init_app(app)

migrate = Migrate()
migrate.init_app(app, db)

engine = db.create_engine(
    f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}",
    {},
)

with app.app_context():
    db.create_all(app=app)


@app.route("/login")
def login():
    if current_user.is_authenticated:
        return jsonify(success=True)
    email = request.args.get("email")
    password = request.args.get("password")
    if email and password:
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash("Logged in successfully.")
            return jsonify(success=True, id=str(user.id))
        return jsonify(success=False, error="wrong email or password")
    return jsonify(success=False, error="missing email or password")


@app.route("/sign_up", methods=["POST"])
def sign_up():
    record = request.json
    email = record.get('email')
    password = record.get('password')
    if email and password:
        return _register_user(email, password)
    return jsonify(success=False)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return jsonify(message="log out")


@app.route("/set_score")
@login_required
def set_score():
    round_id = request.args.get("round_id")
    score = request.args.get("score")
    user_id = request.args.get("user_id")

    player = GameRoundPlayer.query.filter_by(
        user_id=user_id, round_number=round_id
    ).first()
    if player:
        player.passed_date = datetime.utcnow
        player.score = score
        db.session.commit()
        return jsonify(success=True)
    player = GameRoundPlayer(round_number=round_id, user_id=user_id, score=score)
    db.session.add(player)
    db.session.commit()
    return jsonify(error="No score yet or wrong user_id")


@app.route("/get_score")
@login_required
def get_score():
    user_id = request.args.get("user_id")
    player = GameRoundPlayer.query.filter_by(user_id=user_id).first()
    if player:
        return jsonify(player.score)
    return jsonify(error="No score yet or wrong user_id")


# @app.route('/difficulty')
@login_required
def add_difficulty():
    value = request.args.get("value")
    difficulty = Difficulty(value=value)
    if difficulty:
        db.session.add(difficulty)
        db.session.commit()
        return jsonify(f"{difficulty.id}: {difficulty.value}")
    return jsonify(error="Can't add difficulty")


@login_required
def get_difficulty():
    id = request.args.get("id")
    difficulty = Difficulty.query.filter_by(id=id).first()
    if difficulty:
        return jsonify(difficulty.value)
    return jsonify(error="Can't find difficulty")


@app.route("/game", methods=["POST"])
@login_required
def add_game():
    name = request.args.get("name")
    comment = request.args.get("comment")
    game = Game(name=name, comment=comment)
    db.session.add(game)
    db.session.commit()
    return jsonify(success=True, id=game.id)


@app.route("/game", methods=["GET"])
@login_required
def get_game():
    id = request.args.get("id")
    game = Game.query.filter_by(id=id).first()
    if game:
        return jsonify(f"Name = {game.name}, comment = {game.comment}")
    return jsonify("No game with the ID")


@app.route("/game_round", methods=["GET"])
@login_required
def get_game_round():
    id = request.args.get("id")
    game_round = GameRound.query.filter_by(id=id).first()
    if game_round:
        return jsonify(f"Round Number = {game_round.round_number}")
    return jsonify("No game round with the ID")


@app.route("/game_round", methods=["POST"])
@login_required
def set_game_round():
    round_number = request.args.get("round_number")
    difficulty_id = request.args.get("difficulty_id")
    game_id = request.args.get("game_id")
    game_round = GameRound(
        round_number=round_number, difficulty_id=difficulty_id, game_id=game_id
    )
    db.session.add(game_round)
    db.session.commit()
    return jsonify(success=True, id=game_round.id)


@app.route("/game_round_player", methods=["GET"])
@login_required
def get_game_round_player():
    id = request.args.get("user_id")
    game_round_players = GameRoundPlayer.query.filter_by(user_id=id).all()
    if game_round_players:
        result = []
        for player in game_round_players:
            player_res = {"round_id": player.round_number, "score": player.score}
            result.append(player_res)
        return jsonify(result)
    return jsonify("No game_round_player round with the user ID")


@app.route("/game_round_player", methods=["POST"])
@login_required
def set_game_round_player():
    round_id = request.args.get("round_id")
    user_id = request.args.get("user_id")
    score = request.args.get("score")
    game_round_player = GameRoundPlayer(
        round_number=round_id, user_id=user_id, score=score
    )
    db.session.add(game_round_player)
    db.session.commit()
    return jsonify(success=True)
