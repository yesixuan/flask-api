# encoding: utf-8
"""
Created by Vic on 2018/6/24 16:11
"""
from flask import jsonify

from app.libs.redprint import Redprint
from app.libs.token_auth import auth
from app.models.user import User

api = Redprint('user')


class Vic:
    name = 'Vic'
    age = 25

    def __init__(self):
        self.gender = 'male'


@api.route('/<uid>', methods=['GET'])
@auth.login_required
def get_user(uid):
    user = User.query.get_or_404(uid)
    return jsonify(user)
