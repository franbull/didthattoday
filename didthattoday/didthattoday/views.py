from cornice.resource import resource
from pyramid.view import view_config
from pyramid.view import forbidden_view_config
from pyramid.security import authenticated_userid
from pyramid.security import forget
from pyramid.security import remember
from pyramid.httpexceptions import HTTPFound
from pyramid.httpexceptions import HTTPForbidden

from .models import (
    Habit,
    User,
)


def auth_user_id(request):
    if request.environ.get('paste.testing') and request.environ.get('unittest_user_id'):
        return request.environ.get('unittest_user_id')
    else:
        return authenticated_userid(request)


@resource(collection_path='/habits', path='/habit/{id}')
class HabitResource(object):
    def __init__(self, request):
        self.request = request
        self.user = User.from_id(auth_user_id(self.request))
        # I can't think of any reason you should be able to do anything with
        # habits without being logged in? . . . at least until they can be
        # shared I guess? maybe those will be a different kind of habit.
        if self.user is None:
            self.request.errors.add(self.request.url, 'Not logged in.',
                    'You must be logged in to access Habits.')
        # set some variables that the methods might find handy
        self.habit = None
        habit_id = self.request.matchdict.get('id')
        if habit_id is not None:
            habits = [habit for habit in self.user.habits if str(habit.id) == habit_id]
            if not habits:
                self.request.errors.add(self.request.url, 'No such habit.',
                    'There is not habit with id=%s' % habit_id)
            elif len(habits) > 1:
                raise Exception('The database wont let this happen.')
            else:
                self.habit = habits[0]

    def collection_get(self):
        return {'habits': [h.to_json() for h in self.user.habits]}

    def collection_post(self):
        habit = Habit(**self.request.json_body)
        self.user.habits.append(habit)
        return habit.to_json()

    def get(self):
        return self.habit.to_json()

    def put(self):
        for k, v in self.request.json_body.iteritems():
            setattr(self.habit, k, v)
        return self.habit.to_json()


@view_config(route_name='summary', renderer='habitforming.mako')
def summary(request):
    return {'test':'test', 'monkey':'monkey'}


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
