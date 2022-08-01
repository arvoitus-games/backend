import json
import logging
import os

import cv2
import numpy as np
from flask import send_file, request
from flask_restx import Resource, Api, reqparse
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from app import app, add_difficulty, get_difficulty

api = Api(app, version='1.0', title='API title', description='A first version of API')

file_upload = reqparse.RequestParser()
file_upload.add_argument('image',
                         type=FileStorage,
                         location='files',
                         required=True,
                         help='Document 1')
file_upload.add_argument('points', type=str)
from utils.split_picture import crop_one_detail as crop_util


def crop_one_detail():
    logging.error('start_crop')
    data = request.files.get('image')
    points = np.array(json.loads(request.args.get('points')), dtype='int64')
    logging.error(f'points={points}')
    filename = secure_filename(data.filename)
    filepath = os.path.join(app.config['Upload_folder'], filename)
    data.save(filepath)
    part = crop_util(image=cv2.imread(filepath), points=points)
    cv2.imwrite(os.path.join(app.config['Upload_folder'], 'part_' + filename), part)
    return os.path.join(app.config['Upload_folder'], 'part_' + filename)
    # return jsonify(error='image and points fields are necessary')


@api.route('/crop_one_detail')#?image=<image>&points=<points>')
@api.doc(params={'image': 'image', 'points': 'points'})
class MyResource(Resource):
    @api.expect(file_upload)
    def post(self):
        # args = file_upload.parse_args()
        # args['image'].save(os.path.join(app.config['Upload_folder'], secure_filename(args['image'].filename)))
        logging.error('POST')
        return send_file(crop_one_detail(), mimetype='image/png')
        # return {'status': 'Done'}


@api.route('/login', endpoint='Login')
@api.doc(params={'email': 'email', 'password': 'Password'})
class Login(Resource):
    def get(self):
        return {}


@api.route('/sign_up', endpoint='SignUp')
@api.doc(params={'email': 'email', 'password': 'Password'})
class SignUp(Resource):
    def post(self):
        return {}


@api.route('/logout', endpoint='Logout')
@api.doc()
class Logout(Resource):
    def get(self):
        return {}


@api.route('/set_score', endpoint='SetScore')
@api.doc(params={'user_id': 'user ID', 'round_id': 'round ID', 'score': 'score'})
class SetScore(Resource):
    def post(self):
        return {}


@api.route('/get_score', endpoint='GetScore')
@api.doc(params={'user_id': 'user ID'})
class GetScore(Resource):
    def get(self):
        return {}


@api.route('/difficulty', endpoint='Difficulty')
class Difficulty(Resource):
    @api.doc(params={'id': 'difficulty ID'})
    def get(self):
        return get_difficulty()

    @api.doc(params={'value': 'difficulty value'})
    def post(self):
        return add_difficulty()


@api.route('/game', endpoint='GameAPI')
class GameAPI(Resource):
    @api.doc(params={'name': 'Game\'s name', 'comment': 'Comment'})
    def post(self):
        return {}

    @api.doc(params={'id': 'Game\'s ID'})
    def get(self):
        return {}
