# encoding: utf-8
"""
Created by Vic on 2018/6/30 07:54
"""


class AdminScope:
    allow_api = ['v1.super_get_user']


class UserScope:
    allow_api = []


def is_in_scope(scope, endpoint):
    """
    根据类的名字动态地创建类的对象
    globals() 里面保存了 类名：类实体 的 dict 对象
    """
    scope = globals()[scope]()
    if endpoint in scope.allow_api:
        return True
    else:
        return False
