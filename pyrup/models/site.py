from sqlalchemy import (
        Column,
        Integer,
        String,
        )
from sqlalchemy.orm import relationship
from .meta import Base


class Site(Base):
    __tablename__ = 'site'
    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False)
    seq = Column(Integer)
    pages = relationship(
            'Page',
            order_by='Page.seq',
            cascade='all, delete-orphan',
            passive_deletes=True)

    def __init__(self, name, seq=0):
        self.name = name
        self.seq = seq
