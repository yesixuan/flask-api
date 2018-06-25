# encoding: utf-8
"""
Created by Vic on 2018/6/25 08:20
"""
from flask_wtf import Form

from app.libs.error_code import ParameterException


class BaseForm(Form):
    """
    自定义基础验证类，所有校验类都继承这个 Base 类
    """
    def __init__(self, data):
        super(BaseForm, self).__init__(data=data)

    def validate_for_api(self):
        # 自定义验证方法，验证不通过则自动抛出异常
        valid = super(BaseForm, self).validate()
        if not valid:
            # 将 form 中的参数校验错误信息传进去
            raise ParameterException(msg=self.errors)
