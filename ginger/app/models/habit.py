# encoding: utf-8
"""
Created by Vic on 2018/6/24 20:10
"""
from sqlalchemy import Column, Integer, String, SmallInteger, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from app.libs.error_code import NotFound, AuthFailed, Forbidden, Success
from app.models.base import Base, db


class Habit(Base):
    id = Column(Integer, primary_key=True)
    user = relationship('User')
    uid = Column(Integer, ForeignKey('user.id'))
    title = Column(String(24), unique=True, nullable=False)
    desc = Column(String(500), nullable=False)
    period = Column(SmallInteger, default=28)
    done = Column(Boolean, default=False)
    ing = Column(Boolean, default=False)
    remark = Column(String(500), default='')

    def keys(self):
        return ['id', 'uid', 'title', 'desc', 'period', 'done', 'remark', 'ing']

    @staticmethod
    def check_exist(uid, title):
        if Habit.query.filter_by(uid=uid, title=title).first():
            raise Success(msg='已存在该习惯，禁止重复创建', error_code=403)

    @staticmethod
    def create_habit(uid, title, desc, period, remark):
        Habit.check_exist(uid, title)
        with db.auto_commit():
            habit = Habit()
            habit.uid = uid
            habit.title = title
            habit.desc = desc
            habit.period = period
            habit.done = False
            habit.ing = False
            habit.remark = remark
            db.session.add(habit)

