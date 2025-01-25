from sqlalchemy import Column, String, Integer, Table
from common.base import Base

class Password(Base):
    __tablename__ = 'notification'
    id = Column(Integer, primary_key=True)
    fromDepartment = Column(String)
    fromDoctor = Column(String)
    toDepartment = Column(String)
    toDoctor = Column(String)
    data = Column(String)

    def __init__(self, fromDepartment, fromDoctor ,toDepartment ,toDoctor, data):
        self.fromDepartment = fromDepartment
        self.fromDoctor = fromDoctor
        self.toDepartment = toDepartment
        self.toDoctor = toDoctor
        self.data = data