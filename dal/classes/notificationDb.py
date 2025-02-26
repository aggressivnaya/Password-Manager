from sqlalchemy import Column, String, Integer, Table, ForeignKey
from sqlalchemy.orm import relationship
import os
import sys
sys.path.append(os.path.abspath('../..'))
from common.base import Base
#from dal.classes.usersDb import User

class Notification(Base):
    __tablename__ = 'notifications'
    id = Column(Integer, primary_key=True)
    senderId = Column(Integer, ForeignKey("users.id"))
    receiverId = Column(Integer, ForeignKey("users.id"))
    data = Column(String)

    sender = relationship("User", foreign_keys=[senderId], back_populates="sentNotifications")
    receiver = relationship("User", foreign_keys=[receiverId], back_populates="receivedNotifications")

    def __init__(self, senderId, recieverId, data):
        self.senderId = senderId
        self.recieverId = recieverId
        self.data = data