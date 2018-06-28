## 生成 token

生成时机：用户登录成功之后
由哪些要素生成 token：用户的唯一标示、客户端类型、权限作用域、过期时间

1. 根据用户的账户名和密码得到用户的唯一标示
```python
@staticmethod
def verify(email, password):
    user = User.query.filter_by(email=email).first()
    if not user:
        raise NotFound(msg='user not found')
    if not user.check_password(password):
        raise AuthFailed()
    return {'uid': user.id}

def check_password(self, raw):
    if not self._password:
        return False
    return check_password_hash(self._password, raw)
```

2. 生成 token
```python
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

def generate_auth_token(uid, ac_type, scope=None, expiration=7200):
    # 生成令牌
    s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
    return s.dumps({
        'uid': uid,
        'type': ac_type.value  # 客户端类型
    })

token = generate_auth_token(
    identity['uid'], form.type.data, None, expiration
)
t = {
    'token': token.decode('ascii')  # 默认的token并不是字符串
}
```


## 使用 token

思路：在需要登录才能访问的接口前加上校验 token 的装饰器

```python
# encoding: utf-8
"""
Created by Vic on 2018/6/28 06:29
"""
from collections import namedtuple
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired

auth = HTTPBasicAuth()
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
    return User(uid, ac_type, '')

######################在视图函数中加上装饰器###########################

@api.route('/<uid>', methods=['GET'])
@auth.login_required
def get_user(uid):
    return 'i am vic'
```

