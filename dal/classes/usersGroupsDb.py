from sqlalchemy import Column, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship
import os
import sys
sys.path.append(os.path.abspath('../..'))
from common.base import Base
from dal.classes.groupsDb import Group
from dal.classes.usersDb import User

class UserGroup(Base):
    __tablename__ = 'usersGroups'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    userId = Column(Integer, ForeignKey("users.id"))
    groupId = Column(Integer, ForeignKey("group.id"))
    isAdmin = Column(Boolean)

    user = relationship('User', back_populates='groups')
    group = relationship('Group', back_populates='users')

    def __init__(self, userId, groupId, isAdmin=False):
        self.userId = userId
        self.groupId = groupId
        self.isAdmin = isAdmin