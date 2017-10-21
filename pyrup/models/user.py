import bcrypt
from sqlalchemy import (
    Column,
    Integer,
    Text,
)

from .meta import Base


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False, unique=True)
    role = Column(Text, nullable=False)
    failed_count = Column(Integer)
    locked = Column(Integer)

    password_hash = Column(Text)

    def set_password(self, pw):
        pwhash = bcrypt.hashpw(pw.encode('utf8'), bcrypt.gensalt())
        self.password_hash = pwhash.decode('utf8')

    def check_password(self, pw):
        if self.password_hash is not None:
            expected_hash = self.password_hash.encode('utf8')
            return bcrypt.checkpw(pw.encode('utf8'), expected_hash)
        return False

    def is_locked(self):
        return (self.locked == 1)
