from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
import os
import sys
sys.path.append(os.path.abspath('../..'))
from common.base import Base
from dal.classes.passwordDb import Password
from dal.classes.usersDb import User

class UserPassword(Base):
    __tablename__ = 'usersPasswords'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    userId = Column(Integer, ForeignKey("users.id"))
    passwordId = Column(Integer, ForeignKey("passwords.id"))

    user = relationship('User', back_populates='passwords')
    password = relationship('Password', back_populates='users')

    def __init__(self, userId, passwordId):
        self.userId = userId
        self.passwordId = passwordId