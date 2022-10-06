import json
import logging
import os

import cv2
import numpy as np
from flask import send_file, request
from flask_restx import Resource, Api, reqparse, fields

from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from app import app, add_difficulty, get_difficulty
from utils.split_picture import crop_one_detail as crop_util

api = Api(app, version="0.0.1", title="Arvoitus Backend", description="Arvoitus Game Backend API")

file_upload = reqparse.RequestParser()

file_upload.add_argument(
    "image", type=FileStorage, location="files", required=True, help="Document 1"
)
file_upload.add_argument("points", type=str)

def crop_one_detail():
    logging.error("start_crop")
    data = request.files.get("image")
    points = np.array(json.loads(request.args.get("points")), dtype="int64")
    logging.error(f"points={points}")
    filename = secure_filename(data.filename)
    filepath = os.path.join(app.config["Upload_folder"], filename)
    data.save(filepath)
    part = crop_util(image=cv2.imread(filepath), points=points)
    cv2.imwrite(os.path.join(app.config["Upload_folder"], "part_" + filename), part)
    return os.path.join(app.config["Upload_folder"], "part_" + filename)


@api.route("/crop_one_detail")
@api.doc(params={"image": "image", "points": "points"})
class MyResource(Resource):
    @api.expect(file_upload)
    def post(self):
        return send_file(crop_one_detail(), mimetype="image/png")


signup_fields = api.model('SignUp', {
    'email': fields.String,
    'password': fields.String,
    'name': fields.String
})

login_fields = api.model('Login', {
    'email': fields.String,
    'password': fields.String
})

confirm_fields = api.model('EmailConfirm', {
    'token': fields.String
})

@api.route("/login", endpoint="Login")
class Login(Resource):
    @api.doc(body=login_fields)
    def post(self):
        return {}

@api.route("/sign_up", endpoint="SignUp")
class SignUp(Resource):
    @api.doc(body=signup_fields)
    def post(self):
        return {}

@api.route("/confirm/<token>", endpoint="EmailConfirm")
class EmailConfirm(Resource):
    @api.doc(params={"token": "Token"})
    def post(self):
        return {}


@api.route("/logout", endpoint="Logout")
@api.doc()
class Logout(Resource):
    def get(self):
        return {}


@api.route("/set_score", endpoint="SetScore")
@api.doc(params={"user_id": "user ID", "round_id": "round ID", "score": "score"})
class SetScore(Resource):
    def post(self):
        return {}


@api.route("/get_score", endpoint="GetScore")
@api.doc(params={"user_id": "user ID"})
class GetScore(Resource):
    def get(self):
        return {}


@api.route("/difficulty", endpoint="Difficulty")
class Difficulty(Resource):
    @api.doc(params={"id": "difficulty ID"})
    def get(self):
        return get_difficulty()

    @api.doc(params={"value": "difficulty value"})
    def post(self):
        return add_difficulty()


@api.route("/game", endpoint="GameAPI")
class GameAPI(Resource):
    @api.doc(params={"name": "Game's name", "comment": "Comment"})
    def post(self):
        return {}

    @api.doc(params={"id": "Game's ID"})
    def get(self):
        return {}


@api.route("/game_round", endpoint="GameRoundAPI")
class GameRoundAPI(Resource):
    @api.doc(
        params={
            "round_number": "round_number",
            "difficulty_id": "difficulty_id",
            "game_id": "game_id",
        }
    )
    def post(self):
        return {}

    @api.doc(params={"id": "Game round's ID"})
    def get(self):
        return {}


@api.route("/game_round_player", endpoint="GameRoundPlayerAPI")
class GameRoundPlayerAPI(Resource):
    @api.doc(params={"round_id": "round_id", "user_id": "user_id", "score": "score"})
    def post(self):
        return {}

    @api.doc(params={"user_id": "user ID"})
    def get(self):
        return {}
