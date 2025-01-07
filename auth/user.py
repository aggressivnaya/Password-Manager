from sqlalchemy import Column, String, Integer, Table
from common.base import Base

class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String)
    password = Column(String)
    department = Column(String)

    def __init__(self, email, password, department):
        self.email = email
        self.password = password
        self.department = department