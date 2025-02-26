import os
import sys
sys.path.append(os.path.abspath('..'))
from common.base import session_factory
from common.classes import User, Password, UserPassword, Group, UserGroup, Request
'''sys.path.append(os.path.abspath('/dal'))
from classes.groupsDb import Group
from classes.requestDb import Request
from classes.usersDb import User
from classes.passwordDb import Password
from classes.usersGroupsDb import UserGroup
from classes.usersPasswordsDb import UserPassword'''

# Create a new session
db = session_factory()

# Insert some users
user1 = User(username="user1", email="user1@example.com")
user2 = User(username="user2", email="user2@example.com")
db.add(user1)
db.add(user2)

# Insert some passwords
password1 = Password(name="Email Account", password="emailpassword123", shared=False)
password2 = Password(name="Bank Account", password="bankpassword456", shared=True)
db.add(password1)
db.add(password2)

# Insert some groups
group1 = Group(name="Group1", description="This is group 1", link="http://group1.com")
group2 = Group(name="Group2", description="This is group 2", link="http://group2.com")
db.add(group1)
db.add(group2)

# Insert some user-group relationships
user_group1 = UserGroup(userId=user1.id, groupId=group1.id, isAdmin=True)
user_group2 = UserGroup(userId=user2.id, groupId=group2.id, isAdmin=False)
db.add(user_group1)
db.add(user_group2)

# Insert some user-password relationships
user_password1 = UserPassword(userId=user1.id, passwordId=password1.id)
user_password2 = UserPassword(userId=user2.id, passwordId=password2.id)
db.add(user_password1)
db.add(user_password2)

# Insert some requests
request1 = Request(senderId=user1.id, groupId=group1.id, requestCommand="Join group")
request2 = Request(senderId=user2.id, groupId=group2.id, requestCommand="Leave group")

# Commit the changes
db.commit()

print("Data inserted successfully!")