# encoding: utf-8
"""
Created by Vic on 2018/6/25 07:26
自己定义的异常类
"""
from flask import json

from app.libs.error import APIException


class Success(APIException):
    """
    虽然是操作成功类，但是继承 APIException 可以让我们返回的 json 格式保持一致
    """
    code = 201
    msg = 'ok'
    error_code = 0


class DeleteSuccess(Success):
    code = 202
    error_code = -1


class ClientTypeError(APIException):
    # 400 参数错误 401 未授权 403 禁止访问
    # 200 查询成功 201 更新成功 204 删除成功
    code = 400
    msg = 'client is invalid'
    error_code = 1006


class ParameterException(APIException):
    code = 400
    msg = 'invalid parameter'
    error_code = 1000


class NotFound(APIException):
    code = 404
    msg = 'the resource are not_found ┭┮﹏┭┮'
    error_code = 1001


class AuthFailed(APIException):
    code = 401  # 授权失败
    error_code = 1005
    msg = 'authorization failed'


class ServerError(APIException):
    code = 500
    error_code = 999
    msg = 'sorry, we made a mistake o(*￣︶￣*)o'


class Forbidden(APIException):
    code = 403
    error_code = 1004
    msg = 'forbidden, not in scope'
