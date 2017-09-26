from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound, HTTPNotFound
from .abstract_view import AbstractView
from pyrup.forms.site import SiteForm
from ..repositories.site import SiteRepository

MODE_NAME_LIST = {'add': '追加', 'edit': '編集'}


@view_config(
        route_name='site_register',
        request_method='GET',
        renderer='../templates/site_register.jinja2',
        permission='all')
class View(AbstractView):
    def execute(self):
        site_repo = SiteRepository(self.request.dbsession)
        mode = self.request.GET['mode']
        if mode == 'add':
            site_id = ''
            site_list = site_repo.select_list()
            site_name = ''
            site_seq = site_list.count() + 1
        elif mode == 'edit':
            site_id = self.request.GET['site_id']
            site = site_repo.select(site_id)
            site_name = site.name
            site_seq = site.seq
        else:
            return HTTPNotFound()
        form = SiteForm()
        form.site_name.data = site_name
        form.site_seq.data = site_seq
        return {
                'form': form,
                'mode': mode,
                'mode_name': MODE_NAME_LIST.get(mode),
                'site_id': site_id,
                }


@view_config(
        route_name='site_register',
        request_method='POST',
        renderer='../templates/site_register.jinja2',
        permission='all')
class Register(AbstractView):
    def execute(self):
        site_repo = SiteRepository(self.request.dbsession)
        form = SiteForm(self.request.POST)
        mode = self.request.POST['mode']
        if form.validate():
            if mode == 'add':
                site_repo.insert(
                        form.site_name.data,
                        form.site_seq.data)
            elif mode == 'edit':
                site_repo.update(
                        self.request.POST['site_id'],
                        form.site_name.data,
                        form.site_seq.data)
            else:
                return HTTPNotFound()
            return HTTPFound(location='/site/list')
        else:
            if form.site_seq.data is None:
                form.site_seq.data = ''
            return {
                    'form': form,
                    'mode': mode,
                    'mode_name': MODE_NAME_LIST.get(mode),
                    'site_id': self.request.POST['site_id'],
                    }
