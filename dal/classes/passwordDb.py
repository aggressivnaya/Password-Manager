from sqlalchemy import Column, String, Integer, Table
from sqlalchemy.orm import relationship
import os
import sys
sys.path.append(os.path.abspath('../..'))
from common.base import Base
from dal.classes.historyDb import History  # Import the History class

class Password(Base):
    __tablename__ = 'passwords'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    password = Column(String)
    shared = Column(String)

    users = relationship('UserPassword', back_populates='password')
    history = relationship('History', back_populates='password')
    
    def __init__(self, name, password ,shared ):
        self.name = name
        self.password = password
        self.shared = shared
