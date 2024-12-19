from sqlalchemy import Column, String, Integer, ForeignKey, relationship
from common.base import Base
from passwordDb import Password

class History(Base):
    __tablename__ = 'History'
    id = Column(Integer, primary_key=True)
    versionId = Column(Integer)
    passwordId = Column(Integer, ForeignKey(Password.id))
    mehtod = Column(String)
    date = Column(String)

    password = relationship('Password', back_populates='Password')

    def __init__(self, versionId, passwordId, mehtod, date):
        self.versionId = versionId
        self.passwordId = passwordId
        self.mehtod = mehtod
        self.date = date
