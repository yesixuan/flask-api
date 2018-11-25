# encoding: utf-8
"""
Created by Vic on 2018/6/24 20:16
"""
from datetime import datetime
from contextlib import contextmanager

from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy, BaseQuery
from sqlalchemy import Column, Integer, SmallInteger, inspect
from wtforms.ext.sqlalchemy import orm

from app.libs.error_code import NotFound


class SQLAlchemy(_SQLAlchemy):
    @contextmanager
    def auto_commit(self):
        try:
            yield
            self.session.commit()
        except Exception as e:
            db.session.commit()
            raise e


class Query(BaseQuery):
    def filter_by(self, **kwargs):
        if 'status' not in kwargs.keys():
            kwargs['status'] = 1
        return super(Query, self).filter_by(**kwargs)

    def get_or_404(self, ident):
        rv = self.get(ident)
        if rv is None:
            raise NotFound()
        return rv

    def first_or_404(self):
        rv = self.first()
        if rv is None:
            raise NotFound()
        return rv


db = SQLAlchemy(query_class=Query)


class Base(db.Model):
    __abstract__ = True
    create_time = Column(Integer)
    status = Column(SmallInteger, default=1)

    def __init__(self):
        self.create_time = int(datetime.now().timestamp())

    def __getitem__(self, item):
        return getattr(self, item)

    @property
    def create_datetime(self):
        if self.create_time:
            # 将存储在数据库中的整数类型变成 Python 中的时间类型
            return datetime.fromtimestamp(self.create_time)
        else:
            return None

    def set_attrs(self, attrs_dict):
        for key, value in attrs_dict.items():
            if hasattr(self, key) and key != 'id':
                setattr(self, key, value)

    def delete(self):
        self.status = 0


# class MixinJSONSerializer:
#     """
#     更好的 JSON 序列化？
#     """
#     @orm.reconstructor
#     def init_on_load(self):
#         self._field = []
#         self._exclued = []
#
#         self._set_fields()
#         self.__prune_fields()
#
#     def _set_fields(self):
#         pass
#
#     def __prune_fields(self):
#         columns = inspect(self.__class__).columns
#         if not self._fields:
#             all_columns = set(columns.keys())
#             self._fields = list(all_columns - set(self._exclued))
#
#     def hide(self, *args):
#         for key in args:
#             self._fields.remove(key)
#         return self
#
#     def keys(self):
#         return self._fields
#
#     def __getitem__(self, key):
#         return getattr(self, key)
