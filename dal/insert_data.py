import os
import sys
sys.path.append(os.path.abspath('..'))
from common.base import _SessionFactory, session_factory
from common.classes import User, Password, UserPassword, Group, UserGroup, Requestt
from sqlalchemy import insert

# Create a new session

db = _SessionFactory()
session_factory()
'''
# Insert some users
insert_stmt = insert(User).values(username="user1", email="user1@example.com")
db.execute(insert_stmt)
insert_stmt = insert(User).values(username="user2", email="user2@example.com")
db.execute(insert_stmt)


# Insert some passwords
insert_stmt = insert(Password).values(name="Email Account", password="emailpassword123", shared=False)
db.execute(insert_stmt)
insert_stmt = insert(Password).values(name="Bank Account", password="bankpassword456", shared=True)
db.execute(insert_stmt)


# Insert some groups
insert_stmt = insert(Group).values(name="Group1", description="This is group 1", link="http://group1.com")
db.execute(insert_stmt)
insert_stmt = insert(Group).values(name="Group2", description="This is group 2", link='http://group2.com')
db.execute(insert_stmt)

# Insert some user-group relationships

insert_stmt = insert(UserGroup).values(userId=1, groupId=1, isAdmin=True)
db.execute(insert_stmt)
insert_stmt = insert(UserGroup).values(userId=2, groupId=2, isAdmin=False)
db.execute(insert_stmt)

# Insert some user-password relationships
insert_stmt = insert(UserPassword).values(userId=1, passwordId=1)
db.execute(insert_stmt)
insert_stmt = insert(UserPassword).values(userId=2, passwordId=2)
db.execute(insert_stmt)

# Insert some requests
insert_stmt = insert(Requestt).values(sender_id=1, group_id=1, request_command="Join group")
db.execute(insert_stmt)
insert_stmt = insert(Requestt).values(sender_id=2, group_id=2, request_command="Leave group")
db.execute(insert_stmt)
'''
# Commit the changes
db.commit()

print("Data inserted successfully!")
db.close()

# Query the database to check if the data was inserted
'''db = _SessionFactory()
user = (db.query(User).filter(User.username == 'user1').all())[0]
print(user.username + " " + user.email)'''