from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound, HTTPNotFound
from .abstract_view import AbstractView
from pyrup.forms.content import ContentForm
from ..repositories.site import SiteRepository
from ..repositories.page import PageRepository
from ..repositories.content import ContentRepository

MODE_NAME_LIST = {'add': '追加', 'edit': '編集'}
FILENAME_NOTHING = '【なし】'


@view_config(
        route_name='content_register',
        request_method='GET',
        renderer='../templates/content_register.jinja2',
        permission='all')
class View(AbstractView):
    def execute(self):
        site_repo = SiteRepository(self.request.dbsession)
        page_repo = PageRepository(self.request.dbsession)
        content_repo = ContentRepository(self.request.dbsession)
        mode = self.request.GET['mode']
        image_file_id = ''
        image_filename = FILENAME_NOTHING
        attach_file_id = ''
        attach_filename = FILENAME_NOTHING
        if mode == 'add':
            page_id = self.request.GET['page_id']
            content_id = ''
            content_list = content_repo.select_list(page_id)
            content_text = ''
            content_seq = content_list.count() + 1
        elif mode == 'edit':
            content_id = self.request.GET['content_id']
            content, image, attach = content_repo.select(content_id)
            content_text = content.text
            content_seq = content.seq
            if image:
                image_file_id = image.id
                image_filename = image.name
            if attach:
                attach_file_id = attach.id
                attach_filename = attach.name
            page_id = content.page_id
        else:
            return HTTPNotFound()
        page = page_repo.select(page_id)
        site = site_repo.select(page.site_id)
        form = ContentForm()
        form.content_text.data = content_text
        form.content_seq.data = content_seq
        return {
                'form': form,
                'mode': mode,
                'mode_name': MODE_NAME_LIST.get(mode),
                'site_name': site.name,
                'page_id': page_id,
                'page_name': page.name,
                'content_id': content_id,
                'image_file_id': image_file_id,
                'image_filename': image_filename,
                'attach_file_id': attach_file_id,
                'attach_filename': attach_filename,
                }


@view_config(
        route_name='content_register',
        request_method='POST',
        request_param='register',
        renderer='../templates/content_register.jinja2',
        permission='all')
class Register(AbstractView):
    def execute(self):
        content_repo = ContentRepository(self.request.dbsession)
        form = ContentForm(self.request.POST)
        mode = self.request.POST['mode']
        if form.validate():
            asset_dir = self.request.registry.settings['assetdir']
            if self.request.POST['image_file'] is not None\
                    and hasattr(self.request.POST['image_file'], 'file'):
                image_file = self.request.POST['image_file'].file
                image_filename = self.request.POST['image_file'].filename
            else:
                image_file = None
                image_filename = ''
            if self.request.POST['attach_file'] is not None\
                    and hasattr(self.request.POST['attach_file'], 'file'):
                attach_file = self.request.POST['attach_file'].file
                attach_filename = self.request.POST['attach_file'].filename
            else:
                attach_file = None
                attach_filename = ''
            if mode == 'add':
                content_repo.insert(
                        self.request.POST['page_id'],
                        asset_dir,
                        form.content_text.data,
                        image_file,
                        image_filename,
                        attach_file,
                        attach_filename,
                        form.content_seq.data)
            elif mode == 'edit':
                content_repo.update(
                        self.request.POST['content_id'],
                        asset_dir,
                        form.content_text.data,
                        image_file,
                        image_filename,
                        attach_file,
                        attach_filename,
                        form.content_seq.data)
            else:
                return HTTPNotFound()
            return HTTPFound(location='/content/list?page_id='
                    + self.request.POST['page_id'])
        else:
            if form.content_seq.data is None:
                form.content_seq.data = ''
            return {
                    'form': form,
                    'mode': mode,
                    'mode_name': MODE_NAME_LIST.get(mode),
                    'site_name': self.request.POST['site_name'],
                    'page_id': self.request.POST['page_id'],
                    'page_name': self.request.POST['page_name'],
                    'content_id': self.request.POST['content_id'],
                    'image_file_id': self.request.POST['image_file_id'],
                    'image_filename': self.request.POST['image_filename'],
                    'attach_file_id': self.request.POST['attach_file_id'],
                    'attach_filename': self.request.POST['attach_filename'],
                    }


@view_config(
        route_name='content_register',
        request_method='POST',
        request_param='remove_file',
        permission='all')
class RemoveFile(AbstractView):
    def execute(self):
        content_repo = ContentRepository(self.request.dbsession)
        remove_file_type = self.request.POST['remove_file_type']
        if remove_file_type == 'image':
            content_repo.remove_image_file(self.request.POST['content_id'])
        elif remove_file_type == 'attach':
            content_repo.remove_attach_file(self.request.POST['content_id'])
        else:
            return HTTPNotFound()
        return HTTPFound(location='/content/register?mode=edit&content_id='
                + self.request.POST['content_id'])
