# encoding: utf-8
"""
Created by Vic on 2018/6/24 16:11
"""
from flask import jsonify, g

from app.libs.error_code import DeleteSuccess
from app.libs.redprint import Redprint
from app.libs.token_auth import auth
from app.models.base import db
from app.models.user import User

api = Redprint('user')


class Vic:
    name = 'Vic'
    age = 25

    def __init__(self):
        self.gender = 'male'


@api.route('/<uid>', methods=['GET'])
@auth.login_required
def super_get_user(uid):
    user = User.query.get_or_404(uid)
    return jsonify(user)


# 删除用户的 uid 不该由外部导入
@api.route('', methods=['DELETE'])
@auth.login_required
def delete_user():
    # uid 应该通过解析 token 得到用户信息
    uid = g.user.uid
    with db.auto_commit():
        user = User.query.filter_by(id=uid).first_or_404()
        user.delete()
    return DeleteSuccess()
