# encoding: utf-8
"""
Created by Vic on 2018/6/24 19:49
"""
from flask import request

from app.libs.enums import ClientTypeEnum
from app.libs.error_code import ClientTypeError
from app.libs.redprint import Redprint
from app.models.user import User
from app.validators.forms import UserEmailForm, ClientForm

api = Redprint('client')


@api.route('/register', methods=['POST'])
def create_client():
    data = request.json
    form = ClientForm(data=data)
    if form.validate():
        promise = {
            ClientTypeEnum.USER_EMAIL: __register_user_by_email
        }
        promise[form.type.data]()
    else:
        # woforms 抛出的异常不会阻塞程序，只能通过在 else 中抛出自定义异常
        raise ClientTypeError()
    return 'success'


def __register_user_by_email():
    form = UserEmailForm(data=request.json)
    if form.validate():
        User.register_by_email(form.nickname.data, form.account.data, form.secret.data)
