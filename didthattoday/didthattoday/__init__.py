from pyramid.config import Configurator
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from sqlalchemy import engine_from_config

from .models import (
    DBSession,
    Base,
    )


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    authn_policy = AuthTktAuthenticationPolicy(
            settings['auth.secret'],
        )
    authz_policy = ACLAuthorizationPolicy()
    config = Configurator(settings=settings,
        authentication_policy=authn_policy,
        authorization_policy=authz_policy,
    )
    config.include('pyramid_chameleon')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('habits', '/habits')
    config.add_route('habit', '/habit/{id}')
    config.add_route('add_habit', '/habit')
    config.add_route('summary', '/summary')
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')
    config.scan()
    return config.make_wsgi_app()
