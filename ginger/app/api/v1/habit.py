# encoding: utf-8
"""
Created by Vic on 2018/6/24 16:10
"""
from flask import g, jsonify

from app.libs.error_code import Success
from app.libs.redprint import Redprint
from app.libs.response_data import ok
from app.models.base import db
from app.models.habit import Habit
from app.validators.forms import HabitForm
from app.libs.token_auth import auth

api = Redprint('habit')


@api.route('', methods=['POST'])
@auth.login_required
def create_habit():
    form = HabitForm().validate_for_api()
    uid = g.user.uid
    # return jsonify(user)
    Habit.create_habit(uid, form.title.data, form.desc.data, form.period.data, form.remark.data)
    return Success()


@api.route('')
@auth.login_required
def get_habits():
    uid = g.user.uid
    with db.auto_commit():
        habits = Habit.query.filter_by(uid=uid).all()
    return ok(habits)
