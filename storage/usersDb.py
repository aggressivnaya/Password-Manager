from sqlalchemy import Column, String, Integer, Table, relationship
import sqlalchemy as s
from common.base import Base

class User(Base):
    __tablename__ = 'User'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    email = Column(String)

    usersPasswords = relationship('UserPassword', backref='UserPassword.userId',primaryjoin='User.id==UserPassword.userId', lazy='dynamic')
    usersGroup = relationship('UserGroup', backref='UserGroup.userId',primaryjoin='User.id==UserGroup.userId', lazy='dynamic')
    usersRequest = relationship('Request', backref='Request.userId',primaryjoin='User.id==Request.userId', lazy='dynamic')

    def __init__(self, username, email):
        self.username = username
        self.email = email