from sqlalchemy import Column, String, Integer, Table, relationship,ForeignKey
import os
import sys
sys.path.append(os.path.absppath('../..'))
from common.base import Base
from groupsDb import Group
from usersDb import User

class Request(Base):
    __tablename__ = 'Request'
    id = Column(Integer, primary_key=True)
    senderId = Column(Integer, ForeignKey(User.id))
    groupId = Column(Integer, ForeignKey(Group.id))
    requestCommand = Column(String)

    user = relationship('User', back_populates='User')
    group = relationship('Group', back_populates='Group')

    def __init__(self, userId ,managerGroupID , groupId ,requestCommand ):
        self.userId = userId
        self.groupId = groupId
        self.managerGroupID = managerGroupID
        self.requestCommand = requestCommand