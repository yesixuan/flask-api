# encoding: utf-8
"""
Created by Vic on 2018/6/24 16:09
"""


class Redprint:
    """
    红图的特点：
    1. 像蓝图一样注册视图函数
    2. 想蓝图一样支持路径前缀
    3. 可以将自己注册到蓝图上
    """
    def __init__(self, name):
        self.name = name
        self.mound = []

    def route(self, rule, **options):
        def decorator(f):
            # 这里暂时拿不到蓝图对象，所以将参数暂时保存起来
            self.mound.append((f, rule, options))
            return f

        return decorator

    def register(self, bp, url_prefix=None):
        # 如果没有传入 url_prefix，那么默认将宏图的 url_prefix 定义为宏图的名字
        if url_prefix is None:
            url_prefix = '/' + self.name
        for f, rule, options in self.mound:
            endpoint = options.pop("endpoint", f.__name__)
            bp.add_url_rule(url_prefix + rule, endpoint, f, **options)
