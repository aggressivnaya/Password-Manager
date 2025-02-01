from sqlalchemy import Column, Integer, ForeignKey, relationship, Boolean
import os
import sys
sys.path.append(os.path.absppath('../..'))
from common.base import Base
from groupsDb import Group
from usersDb import User

class UserGroup(Base):
    __tablename__ = 'UserGroup'
    id = Column(Integer, primary_key=True)
    userId = Column(Integer, ForeignKey(User.id))
    groupId = Column(Integer, ForeignKey(Group.id))
    isAdmin = Column(Boolean)

    user = relationship('User', back_populates='User')
    group = relationship('Group', back_populates='Group')

    def __init__(self, userId, groupId, isAdmin=False):
        self.userId = userId
        self.groupId = groupId
        self.isAdmin = isAdmin