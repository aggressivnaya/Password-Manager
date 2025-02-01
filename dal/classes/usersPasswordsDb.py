from sqlalchemy import Column, String, Integer, ForeignKey, relationship
import os
import sys
sys.path.append(os.path.absppath('../..'))
from common.base import Base
from passwordDb import Password
from usersDb import User

class UserPassword(Base):
    __tablename__ = 'UserPassword'
    id = Column(Integer, primary_key=True)
    userId = Column(Integer, ForeignKey(User.id))
    passwordId = Column(Integer, ForeignKey(Password.id))

    user = relationship('User', back_populates='User')
    password = relationship('Password', back_populates='Password')

    def __init__(self, userId, passwordId):
        self.userId = userId
        self.passwordId = passwordId