from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from .abstract_view import AbstractView
from ..repositories.site import SiteRepository
from ..repositories.page import PageRepository
from ..repositories.content import ContentRepository


@view_config(
        route_name='content_list',
        request_method='GET',
        renderer='../templates/content_list.jinja2',
        permission='all')
class View(AbstractView):
    def execute(self):
        site_repo = SiteRepository(self.request.dbsession)
        page_repo = PageRepository(self.request.dbsession)
        content_repo = ContentRepository(self.request.dbsession)
        content_list = content_repo.select_list(self.request.GET['page_id'])
        page = page_repo.select(self.request.GET['page_id'])
        site = site_repo.select(page.site_id)
        return {
                'site': site,
                'page': page,
                'content_list': content_list,
                }


@view_config(
        route_name='content_list',
        request_method='POST',
        request_param='content_remove',
        permission='all')
class Remove(AbstractView):
    def execute(self):
        content_repo = ContentRepository(self.request.dbsession)
        content_repo.delete(self.request.POST['remove_content_id'])
        return HTTPFound(location='/content/list?page_id='
                + self.request.POST['page_id'])
