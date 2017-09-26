from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from .abstract_view import AbstractView
from ..repositories.site import SiteRepository
from ..repositories.page import PageRepository


@view_config(
        route_name='page_list',
        request_method='GET',
        renderer='../templates/page_list.jinja2',
        permission='all')
class View(AbstractView):
    def execute(self):
        site_repo = SiteRepository(self.request.dbsession)
        site = site_repo.select(self.request.GET['site_id'])
        return {
                'site_id': site.id,
                'site_name': site.name,
                'page_list': site.pages,
                }


@view_config(
        route_name='page_list',
        request_method='POST',
        request_param='page_remove',
        permission='all')
class Remove(AbstractView):
    def execute(self):
        page_repo = PageRepository(self.request.dbsession)
        page_repo.delete(self.request.POST['remove_page_id'])
        return HTTPFound(location='/page/list?site_id='
                + self.request.POST['site_id'])
