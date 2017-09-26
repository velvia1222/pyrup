import os
import shutil
from ..models import File
from ..utils.format import generate_unique_str


class FileRepository:
    def __init__(self, dbsession):
        self.dbsession = dbsession

    def select(self, id):
        return self.dbsession.query(File).get(id)

    def register(self, srcfileobj, filename, outdir, file=None):
        name, ext = os.path.splitext(filename)
        path = os.path.join(outdir, generate_unique_str() + ext)
        with open(path, 'wb') as dstfileobj:
            shutil.copyfileobj(srcfileobj, dstfileobj)
        if file:
            os.remove(file.path)
            file.path = path
            file.name = filename
        else:
            file = File(path, filename)
            self.dbsession.add(file)
            self.dbsession.flush()
        return file.id

    def remove(self, id):
        file = self.select(id)
        if file:
            os.remove(file.path)
            self.dbsession.delete(file)
