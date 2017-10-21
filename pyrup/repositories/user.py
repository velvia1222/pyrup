from ..models import User


class UserRepository:
    def __init__(self, dbsession):
        self.dbsession = dbsession

    def select(self, name):
        return self.dbsession.query(User).filter_by(name=name).first()
