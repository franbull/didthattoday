from pyramid.response import Response
from pyramid.view import view_config
from pyramid.view import forbidden_view_config
from pyramid.security import authenticated_userid
from pyramid.security import forget
from pyramid.security import remember
from pyramid.httpexceptions import HTTPFound
from pyramid.httpexceptions import HTTPForbidden

from sqlalchemy.exc import DBAPIError

from .models import (
    Habit,
    User,
)

# TODO rather than write our own restful api, why not use cornice?
def auth_user_id(request):
    if request.environ.get('paste.testing') and request.environ.get('unittest_user_id'):
        return request.environ.get('unittest_user_id')
    else:
        return authenticated_userid(request)

@view_config(route_name='home', renderer='templates/mytemplate.pt')
def my_view(request):
    return {'one': 'oh no', 'project': 'didthattoday'}


@view_config(route_name='habits', renderer='json')
def habits(request):
    user = User.from_id(auth_user_id(request))
    if user is None:
        raise Exception('todo')
    return {'habits': [h.to_json() for h in user.habits]}


@view_config(route_name='add_habit', renderer='json', request_method='POST')
def post_habit(request):
    user = User.from_id(auth_user_id(request))
    if user is None:
        raise Exception('todo')
    habit_dict = request.json_body
    habit = Habit(**habit_dict)
    user.habits.append(habit)
    #Habit.Session.add(habit)
    return habit.to_json()


@view_config(route_name='summary', renderer='habitforming.mako')
def summary(request):
    return {'test':'test', 'monkey':'monkey'}

@view_config(route_name='habit', renderer='json', request_method='PUT')
def update_habit(request):
    id = request.matchdict['id']
    habit_dict = request.json_body
    habit = Habit.Session.query(Habit).get(id)
    for k, v in habit_dict.iteritems():
        setattr(habit, k, v)
    return habit.to_json()

@view_config(route_name='habit', renderer='json', request_method='GET')
def get_habit(request):
    id = request.matchdict['id']
    habit = Habit.Session.query(Habit).get(id)
    return habit.to_json()

@forbidden_view_config()
def forbidden_view(request):
    # do not allow a user to login if they are already logged in
    if authenticated_userid(request):
        return HTTPForbidden()

    loc = request.route_url('login', _query=(('next', request.path),))
    return HTTPFound(location=loc)

@view_config(
    route_name='login',
    renderer='login.mako',
)
def login_view(request):
    next = request.params.get('next') or request.route_url('summary')
    login = ''
    did_fail = False
    if 'submit' in request.POST:
        login = request.POST.get('login', '')
        passwd = request.POST.get('passwd', '')

        user = User.Session.query(User).filter(User.login==login).one()
        if user and user.validate_password(passwd):
            headers = remember(request, str(user.id))
            return HTTPFound(location=next, headers=headers)
        did_fail = True

    return {
        'login': login,
        'next': next,
        'failed_attempt': did_fail,
        #'users': USERS,
    }

@view_config(
    route_name='logout',
)
def logout_view(request):
    headers = forget(request)
    loc = request.route_url('home')
    return HTTPFound(location=loc, headers=headers)
