from pyramid.httpexceptions import HTTPFound
from pyramid.security import (
    remember,
    forget,
    )
from pyramid.view import (
    forbidden_view_config,
    view_config,
)
from .abstract_view import AbstractView
from ..repositories.user import UserRepository


MAX_FAILED_COUNT = 5

@view_config(route_name='login', renderer='../templates/login.jinja2')
class Login(AbstractView):
    def execute(self):
        next_url = self.request.params.get('next', self.request.referrer)
        if not next_url:
            next_url = self.request.route_url('site_list')
        message = ''
        login = ''
        if 'form.submitted' in self.request.params:
            user_repo = UserRepository(self.request.dbsession)
            login = self.request.params['login']
            password = self.request.params['password']
            user = user_repo.select(login)
            if user is not None and not user.is_locked():
                if user.check_password(password):
                    user.failed_count = 0
                    headers = remember(self.request, user.id)
                    return HTTPFound(location=next_url, headers=headers)
                else:
                    user.failed_count += 1
                    if user.failed_count >= MAX_FAILED_COUNT:
                        user.locked = 1
            message = 'ログインに失敗しました'

        return dict(
            message=message,
            url=self.request.route_url('login'),
            next_url=next_url,
            login=login,
            )


@view_config(route_name='logout')
class Logout(AbstractView):
    def execute(self):
        headers = forget(self.request)
        next_url = self.request.route_url('login')
        return HTTPFound(location=next_url, headers=headers)


@forbidden_view_config()
class ForbiddenView(AbstractView):
    def execute(self):
        next_url = self.request.route_url('login', _query={'next': self.request.url})
        return HTTPFound(location=next_url)
