# encoding: utf-8
"""
Created by Vic on 2018/6/25 07:26
自己定义的异常类
"""
from app.libs.error import APIException


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
