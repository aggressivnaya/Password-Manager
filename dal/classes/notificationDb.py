from sqlalchemy import Column, String, Integer, Table, ForeignKey, relationship
import os
import sys
sys.path.append(os.path.absppath('../..'))
from common.base import Base
from usersDb import User

class Notification(Base):
    __tablename__ = 'Notification'
    id = Column(Integer, primary_key=True)
    recieverId = Column(Integer, ForeignKey(User.id))
    data = Column(String)

    user = relationship('User', back_populates='User')

    def __init__(self, recieverId, data):
        self.recieverId = recieverId
        self.data = data