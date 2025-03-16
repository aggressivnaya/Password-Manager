from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from common.base import Base, session_factory

class Group(Base):
    __tablename__ = 'group'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    ManagerId = Column(String)
    link = Column(String)
    users = relationship('UserGroup', back_populates='group')
    request2 = relationship('Requestt', back_populates='group')

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, unique=True, nullable=False)
    passwords = relationship('UserPassword', back_populates='user')
    groups = relationship('UserGroup', back_populates='user')
    notifiaction1 = relationship('Notification', foreign_keys="[Notification.sender_id]", back_populates='sender')
    notifiaction2 = relationship('Notification', foreign_keys="[Notification.reciever_id]", back_populates='reciever')
    request1 = relationship('Requestt', back_populates='sender')

class Password(Base):
    __tablename__ = 'password'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    password = Column(String, nullable=False)
    shared = Column(Boolean, default=False)
    users = relationship('UserPassword', back_populates='password')
    history = relationship('History', back_populates='password')

class History(Base):
    __tablename__ = 'history'
    id = Column(Integer, primary_key=True)
    versionId = Column(Integer, nullable=False)
    name = Column(String, nullable=False)
    passwordId = Column(Integer, ForeignKey('password.id'), nullable=False)
    method = Column(String, nullable=False)
    date = Column(String, nullable=False)
    password = relationship('Password', back_populates='history')

class UserGroup(Base):
    __tablename__ = 'user_group'
    id = Column(Integer, primary_key=True)
    userId = Column(Integer, ForeignKey('user.id'), nullable=False)
    groupId = Column(Integer, ForeignKey('group.id'), nullable=False)
    isAdmin = Column(Boolean, default=False)
    user = relationship('User', back_populates='groups')
    group = relationship('Group', back_populates='users')

class UserPassword(Base):
    __tablename__ = 'user_password'
    id = Column(Integer, primary_key=True)
    userId = Column(Integer, ForeignKey('user.id'), nullable=False)
    passwordId = Column(Integer, ForeignKey('password.id'), nullable=False)
    user = relationship('User', back_populates='passwords')
    password = relationship('Password', back_populates='users')

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, ForeignKey("user.id"))
    reciever_id = Column(Integer, ForeignKey("user.id"))
    data = Column(String)

    sender = relationship("User", foreign_keys=[sender_id], back_populates="notifiaction1")
    reciever = relationship("User", foreign_keys=[reciever_id], back_populates="notifiaction2")

    def __init__(self, sender_id, receiver_id, data=""): 
        print("Notification created")

class Requestt(Base):
    __tablename__ = "requests"

    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, ForeignKey("user.id"))
    group_id = Column(Integer, ForeignKey("group.id"))
    request_command = Column(String)

    sender = relationship("User",foreign_keys=[sender_id] , back_populates="request1")
    group = relationship("Group",foreign_keys=[group_id], back_populates="request2")

    def __init__(self, sender_id, group_id, request_command=""):
        print("Request created")

session_factory()