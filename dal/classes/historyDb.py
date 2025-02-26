from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
import os
import sys
sys.path.append(os.path.abspath('../..'))
from common.base import Base
#from dal.classes.passwordDb import Password

class History(Base):
    __tablename__ = 'history'
    id = Column(Integer, primary_key=True)
    versionId = Column(Integer)
    passwordId = Column(Integer, ForeignKey("passwords.id"))
    mehtod = Column(String)
    date = Column(String)

    password = relationship('Password', back_populates='history')

    def __init__(self, versionId, passwordId, mehtod, date):
        self.versionId = versionId
        self.passwordId = passwordId
        self.mehtod = mehtod
        self.date = date
