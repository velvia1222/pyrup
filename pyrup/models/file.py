from sqlalchemy import (
        Column,
        Integer,
        String,
        )
from .meta import Base


class File(Base):
    __tablename__ = 'file'
    id = Column(Integer, primary_key=True)
    path = Column(String(512), nullable=False)
    name = Column(String(64), nullable=False)

    def __init__(self, path, name):
        self.path = path
        self.name = name
