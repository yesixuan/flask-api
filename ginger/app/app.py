# encoding: utf-8
"""
Created by Vic on 2018/6/24 15:39
"""
from datetime import date

from flask import Flask as _Flask
from json import JSONEncoder as _JSONEncoder

from app.libs.error_code import ServerError


class JSONEncoder(_JSONEncoder):
    def default(self, o):
        """default 是可以递归调用的"""
        if hasattr(o, 'keys') and hasattr(o, '__getitem__'):
            return dict(o)
        if isinstance(o, date):
            return o.strftime('%Y-%m-%d')
        raise ServerError()


class Flask(_Flask):
    json_encoder = JSONEncoder



