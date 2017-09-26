import base64
from pyramid.view import view_config
from pyramid.response import FileResponse
from .abstract_view import AbstractView
from ..repositories.file import FileRepository


@view_config(route_name='download', permission='all')
class Download(AbstractView):
    def execute(self):
        file_repo = FileRepository(self.request.dbsession)
        file = file_repo.select(self.request.GET['file_id'])
        response = FileResponse(file.path)
        if self.request.GET['mode'] == 'attach':
            filename = base64.b64encode(bytes(file.name, 'UTF-8')).decode()
            mime_filename = '=?UTF-8?B?' + filename + '?='
            response.content_disposition = 'attachment; filename="'\
                    + mime_filename + '"'
        return response
