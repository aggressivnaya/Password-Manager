from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from common.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)

    passwords = relationship("UserPassword", back_populates="user")
    groups = relationship("UserGroup", back_populates="user")
    sent_notifications = relationship("Notification", foreign_keys="[Notification.sender_id]", back_populates="sender")
    received_notifications = relationship("Notification", foreign_keys="[Notification.receiver_id]", back_populates="receiver")
    sent_requests = relationship("Request", foreign_keys="[Request.sender_id]", back_populates="sender")

    def __init__(self, username="", email=""):
        print("User created")

class Password(Base):
    __tablename__ = "passwords"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    password = Column(String)
    shared = Column(String)

    users = relationship("UserPassword", back_populates="password")
    history = relationship("History", back_populates="password")

    def __init__(self, name="", password="", shared=""):
        print("Password created")

class UserPassword(Base):
    __tablename__ = "usersPasswords"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    password_id = Column(Integer, ForeignKey("passwords.id"))

    user = relationship("User", foreign_keys=[user_id], back_populates="passwords")
    password = relationship("Password", foreign_keys=[password_id], back_populates="users")

    def __init__(self, user_id=-1, password_id=-1):
        print("UserPassword created")

class Group(Base):
    __tablename__ = "group"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    link = Column(String)

    users = relationship("UserGroup",foreign_keys="[UserGroup.group_id]", back_populates="group")
    group_requests = relationship('Request', foreign_keys="[Request.group_id]",back_populates='group')

    def __init__(self, name="", description="", link=""):
        print("Group created")

class UserGroup(Base):
    __tablename__ = "usersGroups"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    group_id = Column(Integer, ForeignKey("group.id"))

    user = relationship("User",foreign_keys=[user_id], back_populates="groups")
    group = relationship("Group", foreign_keys=[group_id], back_populates="users")

    def __init__(self, user_id=-1, group_id=-1, isAdmin=False):
        print("UserGroup created")

class History(Base):
    __tablename__ = "history"

    id = Column(Integer, primary_key=True, index=True)
    version_id = Column(Integer, index=True)
    name = Column(String, index=True)
    password_id = Column(Integer, ForeignKey("passwords.id"))
    method = Column(String)
    date = Column(String)

    password = relationship("Password", foreign_keys=[password_id], back_populates="history")

    def __init__(self, version_id=-1, name="", password_id=-1, method="", date=""):
        print("History created")

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, ForeignKey("users.id"))
    receiver_id = Column(Integer, ForeignKey("users.id"))
    data = Column(String)

    sender = relationship("User", foreign_keys=[sender_id], back_populates="sent_notifications")
    receiver = relationship("User", foreign_keys=[receiver_id], back_populates="received_notifications")

    def __init__(self, sender_id=-1, receiver_id=-1, data=""): 
        print("Notification created")

class Request(Base):
    __tablename__ = "requests"

    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, ForeignKey("users.id"))
    group_id = Column(Integer, ForeignKey("group.id"))
    request_command = Column(String)

    sender = relationship("User",foreign_keys=[sender_id] , back_populates="sent_requests")
    group = relationship("Group",foreign_keys=[group_id], back_populates="group_requests")

    def __init__(self, sender_id=-1, group_id=-1, request_command=""):
        print("Request created")