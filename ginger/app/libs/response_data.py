# encoding: utf-8
"""
Created by Vic on 2018/11/24 17:06
"""
from flask import jsonify


def ok(data=None):
    return jsonify({
        'code': 0,
        'data': data,
        'msg': 'ok'
    })
