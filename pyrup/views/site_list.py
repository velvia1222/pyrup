from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from .abstract_view import AbstractView
from ..repositories.site import SiteRepository


@view_config(
        route_name='site_list',
        request_method='GET',
        renderer='../templates/site_list.jinja2',
        permission='all')
class View(AbstractView):
    def execute(self):
        site_repo = SiteRepository(self.request.dbsession)
        site_list = site_repo.select_list()
        return {'site_list': site_list}


@view_config(
        route_name='site_list',
        request_method='POST',
        request_param='site_remove',
        permission='all')
class Remove(AbstractView):
    def execute(self):
        site_repo = SiteRepository(self.request.dbsession)
        site_repo.delete(self.request.POST['remove_site_id'])
        return HTTPFound(location='/site/list')
