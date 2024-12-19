from sqlalchemy import Column, Integer, ForeignKey, relationship
from common.base import Base
from GroupsDb import Password
from usersDb import User

class UserGroup(Base):
    __tablename__ = 'UserGroup'
    id = Column(Integer, primary_key=True)
    userId = Column(Integer, ForeignKey(User.id))
    groupId = Column(Integer, ForeignKey(Password.id))

    user = relationship('User', back_populates='User')
    group = relationship('Group', back_populates='Group')

    def __init__(self, userId, groupId):
        self.userId = userId
        self.groupId = groupId