import json
import os
from datetime import datetime

import numpy as np
from flask import Flask, flash, request, jsonify
from flask_login import LoginManager, login_required, login_user, logout_user
from flask_login import current_user
from flask_restx import Api, Resource, fields
from werkzeug.datastructures import FileStorage
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename

from models.models import db, User, GameRoundPlayer
from utils.user import _register_user
from utils.split_picture import crop_one_detail as crop_util
from vars import POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_PORT

login_manager = LoginManager()

app = Flask(__name__)

api = Api(app, version='1.0', title='API title', description='A first version of API')

app.secret_key = 'super secret'
uri = os.environ.get('URI')
if uri:
    app.config['SQLALCHEMY_DATABASE_URI'] = uri
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://root:example@localhost:5432'
login_manager.init_app(app)
db.init_app(app)

ns = api.namespace('user', description='User operations')
ns_login = api.namespace('login', description='Auth')


engine = db.create_engine(
    f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}',
    {},
)

with app.app_context():
    db.create_all(app=app)


@app.route('/', methods=['GET', 'POST'])
def index():
    return "Hello"


@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    email = request.args.get('email')
    password = request.args.get('password')
    if email and password:
        return _register_user(email, password)
    return jsonify(success=False)


@login_manager.user_loader
def load_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    return user


@app.route('/login')
def login():
    if current_user.is_authenticated:
        return jsonify(success=True)
    email = request.args.get('email')
    password = request.args.get('password')
    if email and password:
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
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


@app.route('/get_score')
@login_required
def get_score():
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

    player = GameRoundPlayer.query.filter_by(user_id=user_id, round_number=round_id).first()
    if player:
        player.passed_date = datetime.utcnow
        player.score = score
        db.session.commit()
        return jsonify(success=True)
    player = GameRoundPlayer(round_number = round_id, user_id=user_id, score=score)
    db.session.add(player)
    db.session.commit()
    return jsonify(error='No score yet or wrong user_id')


from flask_restx import reqparse
file_upload = reqparse.RequestParser()
file_upload.add_argument('image',
                         type=FileStorage,
                         location='files',
                         required=True,
                         help='Document 1')
app.config['Upload_folder'] = '/app/'


@app.route('/crop_one_detail')
def crop_one_detail():

    image = request.files.get('image')
    points = np.array(request.args.get('points'))
    args = file_upload.parse_args()
    points = np.array(json.dumps(args['points']))
    image = args['image']
    part = crop_util(image, points)
    if part:
        return jsonify(image=part)
    return jsonify(error='image and points fields are necessary')



@api.route('/crop_one_detail?image=<image>&points=<points>')
@api.doc(params={'image': 'image', 'points': 'points'})
class MyResource(Resource):
    @api.expect(file_upload)
    def post(self, image, points):
        args = file_upload.parse_args()
        args['image'].save(os.path.join(app.config['Upload_folder'], secure_filename(args['image'].filename)))
        return {}


# @ns_login.route('/login?email=<email>&password=<password>')
# @ns_login.doc(params={'email': 'email', 'password': 'Password'})
# class Login(Resource):
#     def get(self, email, password):
#         return {}


app.run(host='0.0.0.0', port=os.environ.get("PORT", 5001))
