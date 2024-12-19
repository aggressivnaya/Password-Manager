from sqlalchemy import Column, String, Integer, Table, relationship
from common.base import Base

class Password(Base):
    __tablename__ = 'Password'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    password = Column(String)
    shared = Column(String)

    passwords = relationship('UserPassword', backref='UserPassword.passwordId',primaryjoin='Password.id==UserPassword.passwordId', lazy='dynamic')
    passwordsHistory = relationship('History', backref='History.passwordId',primaryjoin='Password.id==History.passwordId', lazy='dynamic')
    
    def __init__(self, name, password ,shared ):
        self.name = name
        self.password = password
        self.shared = shared
