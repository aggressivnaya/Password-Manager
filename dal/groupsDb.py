from sqlalchemy import Column, Integer, relationship, String
from common.base import Base

class Group(Base):
    __tablename__ = 'Group'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)

    groups = relationship('UserGroup', backref='UserGroup.groupId',primaryjoin='Group.id==UserGroup.groupId', lazy='dynamic')
    groupsRequest = relationship('Request', backref='Request.groupId',primaryjoin='Group.id==Request.groupId', lazy='dynamic')

    def __init__(self, name, description):
        self.name = name
        self.description = description