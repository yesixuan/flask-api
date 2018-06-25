# encoding: utf-8
"""
Created by Vic on 2018/6/24 19:55
"""
from wtforms import Form, StringField, IntegerField
from wtforms.validators import DataRequired, length, Email, Regexp, ValidationError

from app.libs.enums import ClientTypeEnum
from app.models.user import User


class ClientForm(Form):
    account = StringField(validators=[DataRequired(), length(min=5, max=32)])
    secret = StringField()
    type = IntegerField(validators=[DataRequired()])

    def validate_type(self, value):
        # 判断用户传过来的数字是否是我们定义的枚举类型的一种
        try:
            client = ClientTypeEnum(value.data)
        except ValueError as e:
            raise e
        self.type.data = client


class UserEmailForm(ClientForm):
    account = StringField(validators=[Email(message='invalidate email')])
    secret = StringField(validators=[DataRequired(), Regexp(r'^[A-Za-z0-9_*&$#@]{6,22}$')])
    nickname = StringField(validators=[DataRequired(), length(min=2, max=22)])

    def validate_account(self, value):
        if User.query.filter_by(email=value.data).first():
            # 如果邮箱已被注册，那就抛出 wtforms 提供的异常（这里抛出的异常不会导致程序中断，而是会将错误信息方到 form.errors 中）
            raise ValidationError()