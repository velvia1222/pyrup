from sqlalchemy.orm import aliased
from ..models import Content, File
from .file import FileRepository


class ContentRepository:
    def __init__(self, dbsession):
        self.dbsession = dbsession

    def select_list(self, page_id):
        Image = aliased(File)
        Attach = aliased(File)
        return self.dbsession.query(Content, Image, Attach)\
                .outerjoin(Image, Content.image_file_id == Image.id)\
                .outerjoin(Attach, Content.attach_file_id == Attach.id)\
                .filter(Content.page_id == page_id)\
                .order_by(Content.seq)

    def select(self, id):
        Image = aliased(File)
        Attach = aliased(File)
        return self.dbsession.query(Content, Image, Attach)\
                .outerjoin(Image, Content.image_file_id == Image.id)\
                .outerjoin(Attach, Content.attach_file_id == Attach.id)\
                .filter(Content.id == id).first()

    def insert(
            self,
            page_id,
            asset_dir,
            text='',
            image_file=None,
            image_filename='',
            attach_file=None,
            attach_filename='',
            seq=0):

        file_repo = FileRepository(self.dbsession)
        image_file_id = None
        if image_file and image_filename:
            image_file_id = file_repo.register(image_file, image_filename, asset_dir)
        attach_file_id = None
        if attach_file and attach_filename:
            attach_file_id = file_repo.register(attach_file, attach_filename, asset_dir)
        self.dbsession.add(Content(
            page_id,
            text,
            image_file_id,
            attach_file_id,
            seq))

    def update(
            self,
            content_id,
            asset_dir,
            text='',
            image_file=None,
            image_filename='',
            attach_file=None,
            attach_filename='',
            seq=0):
        file_repo = FileRepository(self.dbsession)
        content, image, attach = self.select(content_id)
        content.text = text
        if image_file and image_filename:
            image_file_id = file_repo.register(
                    image_file,
                    image_filename,
                    asset_dir, image)
            content.image_file_id = image_file_id
        if attach_file and attach_filename:
            attach_file_id = file_repo.register(
                    attach_file,
                    attach_filename,
                    asset_dir, attach)
            content.attach_file_id = attach_file_id
        content.seq = seq

    def delete(self, id):
        file_repo = FileRepository(self.dbsession)

        content = self.select(id)[0]
        if not content:
            return

        if content.image_file_id:
            file_repo.remove(content.image_file_id)

        if content.attach_file_id:
            file_repo.remove(content.attach_file_id)

        self.dbsession.delete(content)

    def remove_image_file(self, content_id):
        file_repo = FileRepository(self.dbsession)
        content = self.dbsession.query(Content).get(content_id)
        if content.image_file_id:
            file_repo.remove(content.image_file_id)
            content.image_file_id = None

    def remove_attach_file(self, content_id):
        file_repo = FileRepository(self.dbsession)
        content = self.dbsession.query(Content).get(content_id)
        if content.attach_file_id:
            file_repo.remove(content.attach_file_id)
            content.attach_file_id = None
