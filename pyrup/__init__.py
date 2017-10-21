from pyramid.config import Configurator
from pyramid.session import SignedCookieSessionFactory


def main(global_config, **settings):
    session_factory = SignedCookieSessionFactory(settings['session.secret'], secure=settings['session.secure'], httponly=True)
    config = Configurator(settings=settings)
    config.set_session_factory(session_factory)
    config.set_default_csrf_options(require_csrf=True)
    config.include('pyramid_jinja2')
    config.include('.models')
    config.include('.routes')
    config.include('.security')
    config.scan()
    return config.make_wsgi_app()
