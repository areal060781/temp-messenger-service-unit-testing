import bcrypt

from sqlalchemy import Column, Integer, LargeBinary, Unicode
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import IntegrityError
from nameko_sqlalchemy import DatabaseSession

HASH_WORK_FACTOR = 15
Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    first_name = Column(Unicode(length=128))
    last_name = Column(Unicode(length=128))
    email = Column(Unicode(length=256), unique=True)
    password = Column(LargeBinary())


class UserWrapper:
    def __init__(self, session):
        self.session = session

    def create(self, **kwargs):
        plain_text_password = kwargs['password']
        hashed_password = hash_password(plain_text_password)
        kwargs.update(password=hashed_password)

        user = User(**kwargs)
        self.session.add(user)

        try:
            self.session.commit()
        except IntegrityError as err:
            self.session.rollback()
            error_message = err.args[0]

            if 'already exists' in error_message:
                email = kwargs['email']
                message = 'User already exists - {}'.format(email)
                raise UserAlreadyExists(message)
            else:
                raise CreateUserError(error_message)


class UserStore(DatabaseSession):
    def __init__(self):
        super().__init__(Base)

    def get_dependency(self, worker_ctx):
        database_session = super().get_dependency(worker_ctx)
        return UserWrapper(session=database_session)


class CreateUserError(Exception):
    pass


class UserAlreadyExists(CreateUserError):
    pass


def hash_password(plain_text_password):
    salt = bcrypt.gensalt(rounds=HASH_WORK_FACTOR)
    encoded_password = plain_text_password.encode()

    return bcrypt.hashpw(encoded_password, salt)
