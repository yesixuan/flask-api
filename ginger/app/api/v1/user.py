# encoding: utf-8
"""
Created by Vic on 2018/6/24 16:11
"""
from app.libs.redprint import Redprint

api = Redprint('user')


@api.route('/get')
def get_user():
    return 'i am vic'
