# encoding: utf-8
"""
Created by Vic on 2018/6/24 15:38
"""
from werkzeug.exceptions import HTTPException

from app import create_app
from app.libs.error import APIException

app = create_app()


# 全局的异常拦截，传入异常基类才能拦截所有异常
@app.errorhandler(Exception)
def frame_error(e):
    if isinstance(e, APIException):
        return e
    if isinstance(e, HTTPException):
        code = e.code
        msg = e.description
        error_code = 1007
        return APIException(msg, code, error_code)
    else:
        # 调试模式下显示错误的堆栈信息
        if not app.config('DEBUG'):
            return APIException()
        else:
            raise e


if __name__ == '__main__':
    app.run(debug=True)
