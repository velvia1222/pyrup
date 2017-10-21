from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.security import (
    Authenticated,
    Everyone,
)
from pyramid.session import SignedCookieSessionFactory

from .models import User


class MyAuthenticationPolicy(AuthTktAuthenticationPolicy):
    def authenticated_userid(self, request):
        user = request.user
        if user is not None:
            return user.id

    def effective_principals(self, request):
        principals = [Everyone]
        user = request.user
        if user is not None:
            principals.append(Authenticated)
            principals.append(str(user.id))
            principals.append('role:' + user.role)
        return principals


def get_user(request):
    user_id = request.unauthenticated_userid
    if user_id is not None:
        user = request.dbsession.query(User).get(user_id)
        return user


def includeme(config):
    settings = config.get_settings()
    if settings['session.secure'] == 'False':
        is_secure = False
    else:
        is_secure = True
    session_factory = SignedCookieSessionFactory(
            settings['session.secret'],
            secure=is_secure,
            httponly=True)
    config.set_session_factory(session_factory)
    config.set_default_csrf_options(require_csrf=True)
    authn_policy = MyAuthenticationPolicy(
            settings['auth.secret'],
            secure=is_secure,
            http_only=True)
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(ACLAuthorizationPolicy())
    config.add_request_method(get_user, 'user', reify=True)
