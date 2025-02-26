from sqlalchemy import Column, String, Integer, Table,ForeignKey
from sqlalchemy.orm import relationship
import os
import sys
sys.path.append(os.path.abspath('../..'))
from common.base import Base
#from dal.classes.groupsDb import Group
#from dal.classes.usersDb import User

class Request(Base):
    __tablename__ = 'requests'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    senderId = Column(Integer, ForeignKey("users.id"))
    groupId = Column(Integer, ForeignKey("group.id"))
    requestCommand = Column(String)

    sender = relationship('User', back_populates='sentRequests')
    group = relationship('Group', back_populates='groupRequest')

    def __init__(self, senderId , groupId ,requestCommand ):
        self.senderId = senderId
        self.groupId = groupId
        self.requestCommand = requestCommand