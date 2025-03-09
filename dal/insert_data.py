import os
import sys
sys.path.append(os.path.abspath('..'))
from common.base import _SessionFactory, session_factory
from common.classes import User, Password, UserPassword, Group, UserGroup, Request
from sqlalchemy import insert
'''sys.path.append(os.path.abspath('/dal'))
from classes.groupsDb import Group
from classes.requestDb import Request
from classes.usersDb import User
from classes.passwordDb import Password
from classes.usersGroupsDb import UserGroup
from classes.usersPasswordsDb import UserPassword'''

# Create a new session
db = _SessionFactory()
session_factory()

# Insert some users
user1 = User(username="user1", email="user1@example.com")
user2 = User(username="user2", email="user2@example.com")
insert_stmt = insert(User).values(username=user1.username, email=user1.email)
db.execute(insert_stmt)
insert_stmt = insert(User).values(username=user2.username, email=user2.email)
db.execute(insert_stmt)
#db.add(user1)
#db.add(user2)

# Insert some passwords
password1 = Password(name="Email Account", password="emailpassword123", shared=False)
password2 = Password(name="Bank Account", password="bankpassword456", shared=True)
#db.add(password1)
insert_stmt = insert(Password).values(name=password1.name, password=password1.password, shared=password1.shared)
db.execute(insert_stmt)
insert_stmt = insert(Password).values(name=password2.name, password=password2.password, shared=password2.shared)
db.execute(insert_stmt)
#db.add(password2)

# Insert some groups
group1 = Group(name="Group1", description="This is group 1", link="http://group1.com")
group2 = Group(name="Group2", description="This is group 2", link="http://group2.com")
insert_stmt = insert(Group).values(name=group1.name, description=group1.description, link=group1.link)
db.execute(insert_stmt)
insert_stmt = insert(Group).values(name=group2.name, description=group2.description, link=group2.link)
db.execute(insert_stmt)
#db.add(group1)
#db.add(group2)

# Insert some user-group relationships
user_group1 = UserGroup(user_id=user1.id, group_id=group1.id, isAdmin=True)
user_group2 = UserGroup(user_id=user2.id, group_id=group2.id, isAdmin=False)
#db.add(user_group1)
insert_stmt = insert(UserGroup).values(user_id=user_group1.user_id, group_id=user_group1.group_id, isAdmin=user_group1.isAdmin)
db.execute(insert_stmt)
insert_stmt = insert(UserGroup).values(user_id=user_group2.user_id, group_id=user_group2.group_id, isAdmin=user_group2.isAdmin)
db.execute(insert_stmt)
#db.add(user_group2)

# Insert some user-password relationships
user_password1 = UserPassword(user_id=user1.id, password_id=password1.id)
user_password2 = UserPassword(user_id=user2.id, password_id=password2.id)
#db.add(user_password1)
#db.add(user_password2)
insert_stmt = insert(UserPassword).values(user_id=user_password1.user_id, password_id=user_password1.password_id)
db.execute(insert_stmt)
insert_stmt = insert(UserPassword).values(user_id=user_password2.user_id, password_id=user_password2.password_id)
db.execute(insert_stmt)

# Insert some requests
request1 = Request(sender_id=user1.id, group_id=group1.id, request_command="Join group")
request2 = Request(sender_id=user2.id, group_id=group2.id, request_command="Leave group")
insert_stmt = insert(Request).values(sender_id=request1.sender_id, group_id=request1.group_id, request_command=request1.request_command)
db.execute(insert_stmt)
insert_stmt = insert(Request).values(sender_id=request2.sender_id, group_id=request2.group_id, request_command=request2.request_command)
db.execute(insert_stmt)

# Commit the changes
db.commit()

print("Data inserted successfully!")