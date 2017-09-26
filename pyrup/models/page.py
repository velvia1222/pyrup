from sqlalchemy import (
        Column,
        Integer,
        String,
        ForeignKey,
        )
from sqlalchemy.orm import relationship
from .meta import Base


class Page(Base):
    __tablename__ = 'page'
    id = Column(Integer, primary_key=True)
    site_id = Column(
            Integer,
            ForeignKey('site.id', ondelete='CASCADE'),
            nullable=False)
    name = Column(String(64), nullable=False)
    seq = Column(Integer)
    contents = relationship(
            'Content',
            cascade='all, delete-orphan',
            passive_deletes=True)

    def __init__(self, site_id, name, seq=0):
        self.site_id = site_id
        self.name = name
        self.seq = seq
