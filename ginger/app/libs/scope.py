# encoding: utf-8
"""
Created by Vic on 2018/6/30 07:54
"""


class Scope:
    allow_api = {}
    allow_module = {}
    forbidden = {}

    # 运算符重载
    def __add__(self, other):
        self.allow_api = self.allow_api + other.allow_api
        self.allow_module = self.allow_module + other.allow_module
        self.forbidden = self.forbidden + other.forbidden
        return self


class AdminScope(Scope):
    allow_api = {'v1.super_get_user'}


class UserScope(Scope):
    allow_api = {'v1.A', 'v1.B'}
    # 排除权限
    forbidden = {'v1.C', 'v1.D'}
    allow_module = {'v1.user', 'v1.habit'}


class SuperScope(Scope):
    allow_api = {'V1.C', 'v1.D'}
    allow_module = {'v1.user'}

    def __init__(self):
        # 使用 + 运算符重载
        self + UserScope() + AdminScope()


def is_in_scope(scope, endpoint):
    """
    根据类的名字动态地创建类的对象
    globals() 里面保存了 类名：类实体 的 dict 对象
    """
    scope = globals()[scope]()
    splits = endpoint.split('+')
    red_name = splits[0]

    # 首先验证不可访问权限
    if endpoint in scope.forbidden:
        return False
    if endpoint in scope.allow_api:
        return True
    if red_name in scope.allow_module:
        return True
    else:
        return False
