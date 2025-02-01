from fastapi import FastAPI, Header
from sqlalchemy import update
import jwt
import os
import sys
sys.path.append(os.path.absppath('..'))
from common.base import session_factory, engine, Base
from classes.groupsDb import Group
from classes.historyDb import History
from classes.requestDb import Request
from classes.usersDb import User
from classes.passwordDb import Password
from classes.usersGroupsDb import UserGroup
from classes.usersPasswordsDb import UserPassword

server = FastAPI()
server.config["DATA_SVC_ADDRESS"] = "182.20.1.4:5001"
db = session_factory()
    
@server.post("/changes/add/")
def addPassword(authorization: str = Header(None), password: str = None, name: str = None, shared: str = None):
    currUser = getCurrentUser(authorization.split(' ')[1])

    password = Password(name, password, shared)
    db.add(password)
    return {"success", 200} if db.commit() else {"faild to add", 400}

@server.post("/changes/update/")
def updatePassword(authorization: str = Header(None), currPasswordId: int = None, newPassword: str = None, newName: str = None, shared: str = None):
    currUser = getCurrentUser(authorization.split(' ')[1])

    #query that updates the password by id
    stmt = (
            update(Password)
            .where(Password.id == currPasswordId)
            .values(password=newPassword, name=newName, shared=shared)
        )

    db.execute(stmt)
    return {"success", 200} if db.commit() else {"faild to update", 400}

@server.delete("/changes/delete/")
def deletePassword(authorization: str = Header(None), currPasswordId: int = None):
    currUser = getCurrentUser(authorization.split(' ')[1])

    password = (db.query(Password).filter(Password.id == currPasswordId).all())[0]
    db.delete(password)
    return {"success", 200} if db.commit() else {"faild to delete", 400}
    
@server.get("/getPassword")
def getRequiredPassword(passwordId: int = None):
    #finding the password by id
    password = (db.query(Password).filter(Password.id == passwordId).all())[0]
    return {"password": password}

@server.get("/getPasswords")
def getUserPasswords(authorization: str = Header(None)):
    #finding by the user all his passwords
    currUser = getCurrentUser(authorization.split(' ')[1])

    passwords = (
        db.query(Password)
        .join(UserPassword, Password.id == UserPassword.passwordId)
        .filter(UserPassword.userId == currUser.id)
        .all()
    )

    # Return a list of password details
    return [{"id": password.id, "name": password.name, "password": password.password} for password in passwords]
    
@server.get("/history")
def history(authorization: str = Header(None)):
    #tokenData = authorization.split(' ')[1]
    #username = request.args.get('username', type = str)
    #user = (db.query(User).filter(User.username == username).all())[0]
    currUser = getCurrentUser(authorization.split(' ')[1])

    result = (
        db.query(History)
        .join(Password, Password.id == History.passwordId)
        .join(UserPassword, UserPassword.passwordId == Password.id)
        .filter(UserPassword.userId == currUser.id)
        .all()
    )#lst of history objects

    if result:
        {"error":"faild to get history"}

    return result

@server.post("/group/create_group")
def createGroup(authorization: str = Header(None), name: str = None, description: str = None):
    #username = request.args.get('username', type = str)
    #user = (db.query(User).filter(User.username == username).all())[0]
    currUser = getCurrentUser(authorization.split(' ')[1])

    #creating the group
    group = Group(name, description)
    db.add(group)
    db.commit()

    #adding the user to the group
    group = (db.query(Group).filter(Group.name == name and Group.description == description).all())[0]
    userGroup = UserGroup(currUser.id, group.id, True)
    db.add(userGroup)
    return {"success", 200} if db.commit() else {"faild to create room", 400}

@server.get("/group/enter_group")
def enterGroup(authorization: str = Header(None), groupLink: str = None):
    '''sending request to admin user then waiting when admin accept'''

    #username = request.args.get('username', type = str)
    #user = (db.query(User).filter(User.username == username).all())[0]
    currUser = getCurrentUser(authorization.split(' ')[1])

    group = (db.query(Group).filter(Group.link == groupLink).all())[0]

    #finding the admin of the group
    userGroup = (db.query(UserGroup).filter(UserGroup.groupId == group.id and UserGroup.isAdmin == True).all())[0]
    request = Request(currUser.id, userGroup.userId, group.id)#creating an request to join to the group
    db.add(request)
    return {"success", 200} if db.commit() else {"faild to enter group", 400}

@server.post("/group/accept_user")
def acceptUser(authorization: str = Header(None)):
    #Admin is accepting the request of user to enter to group
    currUser = getCurrentUser(authorization.split(' ')[1])
    #adminUsername = request.args.get('adminUsername', type = str)#TODO: check with token
    username = request.args.get('username', type = str)
    user = (db.query(User).filter(User.username == username).all())[0]

    groupName = request.args.get('group_name', type = str)
    group = (db.query(Group).filter(Group.name == groupName).all())[0]

    request = (db.query(Request).filter(Request.groupId == group.id and Request.senderId == user.id).all())[0]

    # Find the manager of the group (isAdmin=True in UserGroup)
    manager = (
        db.query(UserGroup)
        .filter(UserGroup.groupId == request.groupId, UserGroup.isAdmin == True)
        .first()
    )
    if not manager:
        print(f"No manager found for group ID {request.groupId}.")
        return False
    
    # Add the user to the group
    new_user_group = UserGroup(userId=request.senderId, groupId=request.groupId, isAdmin=False)
    db.add(new_user_group)
    
    # Delete the request
    db.delete(request)
    
    return {"success", 200} if db.commit() else {"faild to accept user to group", 400}

@server.delete("/group/leave_group")
def leaveGroup(authorization: str = Header(None), groupName: str = None):
    #username = request.args.get('username', type = str)
    #user = (db.query(User).filter(User.username == username).all())[0]
    currUser = getCurrentUser(authorization.split(' ')[1])

    group = (db.query(Group).filter(Group.name == groupName).all())[0]

    userGroup = UserGroup(currUser.id, group.id)
    db.delete(userGroup)
    
    return {"success", 200} if db.commit() else {"faild to leave roo", 400}

@server.route("/group/remove_user", methods=["DELETE"])
def removeGroup(authorization: str = Header(None), groupName: str = None):
    currUser = getCurrentUser(authorization.split(' ')[1])
    #adminUsername = request.args.get('adminUsername', type = str)
    group = (db.query(Group).filter(Group.name == groupName).all())[0]

    # Delete references to the group in the UserGroup table
    db.query(UserGroup).filter(UserGroup.groupId == group.id).delete()
    
    # Delete the group itself
    db.query(Group).filter(Group.id == group.id).delete()
    
    return {"success", 200} if db.commit() else {"faild to delete group", 400}

@server.get("/group")
def groupInfo(groupName: str = None):
    group = (db.query(Group).filter(Group.name == groupName).all())[0]
    #getting the users that in the group
    usersInGroup = getUsersOfGroup(group)

    #getting the passwords that in the group
    sharedPasswords = getAllSharedPasswordsOfGroup(usersInGroup)

    groupInfo = {"name": group.name, "description": group.description, "users": usersInGroup, "shared_passwords": sharedPasswords}
    
    if not groupInfo:
        return {"error": "error with group info"}
    return groupInfo

@server.delete("/logout")
def logout(authorization: str = Header(None)):
    #loging out from the app complitely
    #username = request.args.get('username', type = str)
    #user = (db.query(User).filter(User.username == username).all())[0]
    currUser = getCurrentUser(authorization.split(' ')[1])
    db.delete(currUser)
    return ("success", 200) if db.commit() else ("faild to logout", 400)

def getCurrentUser(token):
    # Get the username from the token
    token = token.split(" ")[1]
    username = jwt.decode(token, "SARCASM", algorithms=["HS256"])["username"]

    return (db.query(User).filter(User.username == username).all())[0]

def getUsersOfGroup(group):
    usersInGroup = []
    # Get all users in the group
    usersId = db.query(UserGroup.userId).filter(UserGroup.groupId == group.id).all()
    usersId = [u[0] for u in usersId]  # Extract user IDs
    for userId in usersId:
        user = (db.query(User).filter(User.id == userId).all())[0]#getting the user obj
        usersInGroup.append(user)

    return [{"id":user.id, "username": user.username, "email": user.email} for user in usersInGroup]

def getAllSharedPasswordsOfGroup(users):
    usersId = [u["id"]for u in users]

    # Get all shared passwords for these users
    shared_passwords = (db.query(Password).join(UserPassword, Password.id == UserPassword.passwordId).filter(UserPassword.userId.in_(usersId), Password.shared == True).all())

    # Return the dict in list of shared passwords
    return [{"id": pw.id, "name": pw.name, "password": pw.password} for pw in shared_passwords]

if __name__ == "__main__":
    server.run(host="182.20.1.4", port=5001)
    #127.0.0.1
    #182.20.1.4