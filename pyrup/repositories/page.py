from ..models import Page
from .content import ContentRepository


class PageRepository:
    def __init__(self, dbsession):
        self.dbsession = dbsession

    def select_list(self, site_id):
        return self.dbsession.query(Page)\
                .filter(Page.site_id == site_id)\
                .order_by(Page.seq, Page.name)

    def select(self, id):
        return self.dbsession.query(Page).get(id)

    def insert(self, site_id, name, seq=0):
        page = Page(site_id, name, seq)
        self.dbsession.add(page)
        self.dbsession.flush()
        return page.id

    def update(self, id, name, seq=0):
        page = self.select(id)
        page.name = name
        page.seq = seq

    def delete(self, id):
        content_repo = ContentRepository(self.dbsession)

        page = self.select(id)
        if not page:
            return

        for content in page.contents:
            content_repo.delete(content.id)

        self.dbsession.delete(page)
