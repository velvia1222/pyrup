from sqlalchemy import (
        Column,
        Integer,
        Text,
        ForeignKey,
        )
from .meta import Base


class Content(Base):
    __tablename__ = 'content'
    id = Column(Integer, primary_key=True)
    page_id = Column(
            Integer,
            ForeignKey('page.id', ondelete='CASCADE'),
            nullable=False)
    text = Column(Text)
    image_file_id = Column(Integer, ForeignKey('file.id'))
    attach_file_id = Column(Integer, ForeignKey('file.id'))
    seq = Column(Integer)

    def __init__(
            self,
            page_id,
            text='',
            image_file_id=None,
            attach_file_id=None,
            seq=0):
        self.page_id = page_id
        self.text = text
        self.image_file_id = image_file_id
        self.attach_file_id = attach_file_id
        self.seq = seq
