from sqlalchemy import Column, Integer, Unicode
from sqlalchemy.ext.declarative import declarative_base
from nameko_sqlalchemy import DatabaseSession

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    first_name = Column(Unicode(length=128))
    last_name = Column(Unicode(length=128))
    email = Column(Unicode(length=256), unique=True)
    password = Column(Unicode(length=512))


class UserWrapper:
    def __init__(self, session):
        self.session = session

    def create(self, **kwargs):
        user = User(**kwargs)
        self.session.add(user)
        self.session.commit()


class UserStore(DatabaseSession):
    def __init__(self):
        super().__init__(Base)

    def get_dependency(self, worker_ctx):
        database_session = super().get_dependency(worker_ctx)
        return UserWrapper(session=database_session)
