# encoding: utf-8
"""
Created by Vic on 2018/6/28 06:29
"""
from collections import namedtuple
from flask import current_app, g, request
from flask_httpauth import HTTPBasicAuth
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired

from app.libs.error_code import AuthFailed, Forbidden
from app.libs.scope import is_in_scope

auth = HTTPBasicAuth()
# 用 namedtuple 的原因在于在取值的时候可以用 . 取值，而字典只能用 [] 取值
User = namedtuple('User', ['uid', 'ac_type', 'scope'])


@auth.verify_password
def verify_password(token, password):
    """
    account 与 password 是需要客户端从 http 请求头部中携带过来
    这个特别的 header 必须遵循以下标准：
    key = Authorization
    value = basic base64(vic:123456)
    我们不需要传递账户、密码，但是我们可以通过账户来传递 token
    """
    user_info = verify_auth_token(token)
    if not user_info:
        return False
    else:
        # g 变量的用处，暂时不明
        g.user = user_info
        return True


def verify_auth_token(token):
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
    except BadSignature:
        # token 不合法
        raise AuthFailed(msg='token is invalid', error_code=1002)
    except SignatureExpired:
        # token 过期
        raise AuthFailed(msg='token is expired', error_code=1002)
    uid = data['uid']
    ac_type = data['type']
    scope = data['scope']
    # 传入当前权限与视图函数
    allow = is_in_scope(scope, request.endpoint)
    if not allow:
        raise Forbidden()
    return User(uid, ac_type, scope)
