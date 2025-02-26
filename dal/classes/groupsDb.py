from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
import os
import sys
sys.path.append(os.path.abspath('../..'))
from common.base import Base
from dal.classes.usersGroupsDb import UserGroup  # Import the UserGroup class
from dal.classes.requestDb import Request  # Import the Request class


class Group(Base):
    __tablename__ = 'group'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    link = Column(String)

    groups = relationship('UserGroup', back_populates='group')
    groupRequest = relationship('Request', back_populates='group')

    def __init__(self, name, description, link):
        self.name = name
        self.description = description
        self.link = link