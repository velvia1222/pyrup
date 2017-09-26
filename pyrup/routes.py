from pyramid.security import (
    Allow,
)

def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')
    config.add_route('download', '/download', factory=site_factory)
    config.add_route('site_list', '/site/list', factory=site_factory)
    config.add_route('site_register', '/site/register', factory=site_factory)
    config.add_route('page_list', '/page/list', factory=site_factory)
    config.add_route('page_register', '/page/register', factory=site_factory)
    config.add_route('content_list', '/content/list', factory=site_factory)
    config.add_route('content_register', '/content/register', factory=site_factory)


def site_factory(request):
    return SiteResource()


class SiteResource:
    def __acl__(self):
        return [
                (Allow, 'role:gooduser', 'all'),
        ]
