from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from .models import (
    Habit,
)


@view_config(route_name='home', renderer='templates/mytemplate.pt')
def my_view(request):
    return {'one': 'oh no', 'project': 'didthattoday'}


@view_config(route_name='habits', renderer='json')
def habits(request):
    return {'habits': [h.to_json() for h in Habit.Session.query(Habit).all()]}


@view_config(route_name='add_habit', renderer='json', request_method='POST')
def post_habit(request):
    habit_dict = request.json_body
    habit = Habit(**habit_dict)
    Habit.Session.add(habit)
    return habit.to_json()


@view_config(route_name='summary', renderer='templates/habitforming.pt')
def summary(request):
    return {'test':'test', 'monkey':'monkey'}