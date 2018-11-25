# encoding: utf-8
"""
Created by Vic on 2018/6/25 07:44
"""
from flask import request, json
from werkzeug.exceptions import HTTPException


class APIException(HTTPException):
    code = 500
    msg = 'sorry, wo make a mistake (o(*￣︶￣*)o)!'
    error_code = 999

    def __init__(self, msg=None, code=None, error_code=None, headers=None):
        if code:
            self.code = code
        if error_code:
            self.error_code = error_code
        if msg:
            self.msg = msg
        super(APIException, self).__init__(msg, None)

    def get_body(self, environ=None):
        body = dict(
            msg=self.msg,  # 这里的 msg 用来接收 form 的 errors 信息
            error_code=self.error_code,
            request=request.method + ' ' + self.get_url_no_param()
        )
        text = json.dumps(body)
        return text

    def get_headers(self, environ=None):
        return [
            ('Content-Type', 'application/json'),
            ('Access-Control-Allow-Origin', '*'),
            ('Access-Control-Allow-Methods', '*'),
            ('Access-Control-Allow-Headers', '*')
        ]

    @staticmethod
    def get_url_no_param():
        # 获取请求接口地址
        full_path = str(request.full_path)
        main_path = full_path.split('?')
        return main_path[0]
