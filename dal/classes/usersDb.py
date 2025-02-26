from sqlalchemy import Column, String, Integer, Table
from sqlalchemy.orm import relationship
import os
import sys
sys.path.append(os.path.abspath('../..'))
from common.base import Base
from dal.classes.notificationDb import Notification  # Import the Notification class

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    email = Column(String)

    passwords = relationship('UserPassword', back_populates='user')
    groups = relationship('UserGroup', back_populates='user')
    sentNotifications = relationship('Notification', foreign_keys=[Notification.senderId], back_populates='sender')
    receivedNotifications = relationship('Notification', foreign_keys=[Notification.receiverId], back_populates='receiver')
    sentRequests = relationship('Request', back_populates='sender')

    def __init__(self, username, email):
        self.username = username
        self.email = email