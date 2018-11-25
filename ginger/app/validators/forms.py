# encoding: utf-8
"""
Created by Vic on 2018/6/24 19:55
"""
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, length, Email, Regexp, ValidationError

from app.libs.enums import ClientTypeEnum
from app.models.user import User
from app.validators.base import BaseForm


class ClientForm(BaseForm):
    account = StringField(validators=[DataRequired(message='不允许为空'), length(min=5, max=32)])
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
            raise ValidationError('邮箱已被注册！！！')

    def validate_nickname(self, value):
        if User.query.filter_by(nickname=value.data).first():
            raise ValidationError('昵称已被占用！！！')


class HabitForm(BaseForm):
    title = StringField(validators=[DataRequired(message='习惯名必填'), length(min=1, max=24)])
    desc = StringField(validators=[DataRequired(message='习惯描述不允许为空'), length(min=1, max=500)])
    period = IntegerField(validators=[DataRequired(message='习惯周期必填')])
    remark = StringField(validators=[length(max=500)])
