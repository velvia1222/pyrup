from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound, HTTPNotFound
from .abstract_view import AbstractView
from pyrup.forms.page import PageForm
from ..repositories.site import SiteRepository
from ..repositories.page import PageRepository

MODE_NAME_LIST = {'add': '追加', 'edit': '編集'}


@view_config(
        route_name='page_register',
        request_method='GET',
        renderer='../templates/page_register.jinja2',
        permission='all')
class View(AbstractView):
    def execute(self):
        site_repo = SiteRepository(self.request.dbsession)
        page_repo = PageRepository(self.request.dbsession)
        mode = self.request.GET['mode']
        if mode == 'add':
            site_id = self.request.GET['site_id']
            page_list = page_repo.select_list(site_id)
            page_id = ''
            page_name = ''
            page_seq = page_list.count() + 1
        elif mode == 'edit':
            page_id = self.request.GET['page_id']
            page = page_repo.select(page_id)
            page_name = page.name
            page_seq = page.seq
            site_id = page.site_id
        else:
            return HTTPNotFound()
        site = site_repo.select(site_id)
        site_name = site.name
        form = PageForm()
        form.page_name.data = page_name
        form.page_seq.data = page_seq
        return {
                'form': form,
                'mode': mode,
                'mode_name': MODE_NAME_LIST.get(mode),
                'site_id': site_id,
                'site_name': site_name,
                'page_id': page_id,
                }


@view_config(
        route_name='page_register',
        request_method='POST',
        renderer='../templates/page_register.jinja2',
        permission='all')
class Register(AbstractView):
    def execute(self):
        page_repo = PageRepository(self.request.dbsession)
        form = PageForm(self.request.POST)
        mode = self.request.POST['mode']
        if form.validate():
            if mode == 'add':
                page_repo.insert(
                        self.request.POST['site_id'],
                        form.page_name.data,
                        form.page_seq.data)
            elif mode == 'edit':
                page_repo.update(
                        self.request.POST['page_id'],
                        form.page_name.data,
                        form.page_seq.data)
            else:
                return HTTPNotFound()
            return HTTPFound(location='/page/list?site_id='
                    + self.request.POST['site_id'])
        else:
            if form.page_seq.data is None:
                form.page_seq.data = ''
            return {
                    'form': form,
                    'mode': mode,
                    'mode_name': MODE_NAME_LIST.get(mode),
                    'site_id': self.request.POST['site_id'],
                    'site_name': self.request.POST['site_name'],
                    'page_id': self.request.POST['page_id'],
                    }
