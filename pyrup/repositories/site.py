from ..models import Site
from .page import PageRepository


class SiteRepository:
    def __init__(self, dbsession):
        self.dbsession = dbsession

    def select_list(self):
        return self.dbsession.query(Site).order_by(Site.seq, Site.name)

    def select(self, id):
        return self.dbsession.query(Site).get(id)

    def insert(self, name, seq=0):
        site = Site(name, seq)
        self.dbsession.add(site)
        self.dbsession.flush()
        return site.id

    def update(self, id, name, seq=0):
        site = self.select(id)
        site.name = name
        site.seq = seq

    def delete(self, id):
        page_repo = PageRepository(self.dbsession)

        site = self.select(id)
        if not site:
            return

        for page in site.pages:
            page_repo.delete(page.id)

        self.dbsession.delete(site)
