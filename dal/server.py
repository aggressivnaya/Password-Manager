import random
from fastapi import FastAPI, Header, Request, Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import update, insert, delete
from typing import Annotated
import jwt
import os
import sys
sys.path.append(os.path.abspath('..'))
from common.base import session_factory, engine, Base, _SessionFactory
from common.classes import User, Password, UserPassword, Group, UserGroup, Requestt, History
'''from classes.groupsDb import Group
from classes.historyDb import History
from classes.requestDb import Request
from classes.usersDb import User
from classes.passwordDb import Password
from classes.usersGroupsDb import UserGroup
from classes.usersPasswordsDb import UserPassword'''

server = FastAPI()
db = _SessionFactory()
session_factory()
server.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
oauth2Schema = OAuth2PasswordBearer(tokenUrl="placeholder")
    
@server.post("/changes/add/")
def addPassword(request: Request, token: Annotated[str, Depends(oauth2Schema)], password: str = None, name: str = None, shared: str = None):
    currUser = getCurrentUser(token)

    #password = Password(name, password, shared)
    insert_stmt = insert(Password).values(name=name, password=password, shared=shared)
    #db.add(password)
    db.execute(insert_stmt)
    db.commit()

    password = (db.query(Password).filter(Password.name == name and Password.password == password and Password.shared == shared).all())[0]
    #userPassword = UserPassword(currUser.id, password.id)
    insert_stmt = insert(UserPassword).values(user_id=currUser.id, password_id=password.id)
    db.execute(insert_stmt)

    try: 
        db.commit()
        return {"success", 200}
    except Exception as e:
        print('exception in addPassword:', e)
        raise e

@server.post("/changes/update/")
def updatePassword(request: Request, token: Annotated[str, Depends(oauth2Schema)], currPasswordId: int = None, newPassword: str = None, newName: str = None, shared: str = None):
    #currUser = getCurrentUser(token)

    #query that updates the password by id
    stmt = (
            update(Password)
            .where(Password.id == currPasswordId)
            .values(password=newPassword, name=newName, shared=shared)
        )

    db.execute(stmt)

    try:
        db.commit()
        return {"success", 200}
    except Exception as e:
        print('exception in updatePassword:', e)
        raise e

@server.delete("/changes/delete/")
def deletePassword(request: Request, token: Annotated[str, Depends(oauth2Schema)], currPasswordId: int = None):
    currUser = getCurrentUser(token)

    #password = (db.query(Password).filter(Password.id == currPasswordId).all())[0]
    
    #passwordFromUsrPass = (db.query(UserPassword).filter(UserPassword.passwordId == password.id and UserPassword.user_id == currUser.id).all())[0]
    #db.delete(passwordFromUsrPass)
    delete_stmt = delete(Password).where(Password.id == currPasswordId)
    db.execute(delete_stmt)
    db.commit()
    delete_stmt = delete(UserPassword).where(UserPassword.passwordId == currPasswordId and UserPassword.user_id == currUser.id)
    db.execute(delete_stmt)
    #db.delete(password)

    try:
        db.commit()
        return {"success", 200}
    except Exception as e:
        print('exception in deletePassword:', e)
        raise e
    
@server.get("/getPassword")
def getRequiredPassword(passwordId: int = None):
    #finding the password by id
    password = (db.query(Password).filter(Password.id == passwordId).all())[0]
    return {"password": password}

@server.get("/getPasswords")
def getUserPasswords(request: Request, token: Annotated[str, Depends(oauth2Schema)]):
    #finding by the user all his passwords
    currUser = getCurrentUser(token)

    passwords = (
        db.query(Password)
        .join(UserPassword, Password.id == UserPassword.passwordId)
        .filter(UserPassword.user_id == currUser.id)
        .all()
    )

    # Return a list of password details
    return {'passwords': [{"id": password.id, "name": password.name, "password": password.password} for password in passwords]} 
    
@server.get("/history")
def history(request: Request, token: Annotated[str, Depends(oauth2Schema)]):
    #tokenData = authorization.split(' ')[1]
    #username = request.args.get('username', type = str)
    #user = (db.query(User).filter(User.username == username).all())[0]
    currUser = getCurrentUser(token)

    result = (
        db.query(History)
        .join(Password, Password.id == History.passwordId)
        .join(UserPassword, UserPassword.passwordId == Password.id)
        .filter(UserPassword.user_id == currUser.id)
        .all()
    )#lst of history objects

    if result:
        {"error":"faild to get history"}

    return {'history':result}

@server.post("/group/create_group")
def createGroup(request: Request, token: Annotated[str, Depends(oauth2Schema)], name: str = None, description: str = None):
    currUser = getCurrentUser(token)

    isGroup = (db.query(Group).filter(Group.name == name).all())
    if isGroup:
        return {"error": "Group already exists"}
    
    #creating the group
    link = name + str(random.randint(100000, 999999))
    insert_stmt = insert(Group).values(name=name, description=description, link=link)
    db.execute(insert_stmt)
    #group = Group(name, description, "link")
    #db.add(group)
    db.commit()

    #adding the user to the group
    group = (db.query(Group).filter(Group.name == name and Group.description == description).all())[0]
    insert_stmt = insert(UserGroup).values(user_id=currUser.id, group_id=group.id, isAdmin=True)
    #userGroup = UserGroup(currUser.id, group.id, True)
    #db.add(userGroup)
    db.execute(insert_stmt)

    try:
        db.commit()
        return {"success", 200}
    except Exception as e:
        print('exception in createGroup:', e)
        raise e

@server.get("/group/enter_group")
def enterGroup(request: Request, token: Annotated[str, Depends(oauth2Schema)], groupLink: str = None):
    '''sending request to admin user then waiting when admin accept'''

    #username = request.args.get('username', type = str)
    #user = (db.query(User).filter(User.username == username).all())[0]
    currUser = getCurrentUser(token)

    group = (db.query(Group).filter(Group.link == groupLink).all())[0]

    #finding the admin of the group
    userGroup = (db.query(UserGroup).filter(UserGroup.groupId == group.id and UserGroup.isAdmin == True).all())[0]
    insert_stmt = insert(Requestt).values(senderId=currUser.id, receiverId=userGroup.user_id, groupId=group.id)
    #request = Request(currUser.id, userGroup.user_id, group.id)#creating an request to join to the group
    #db.add(request)
    db.execute(insert_stmt)

    try:
        db.commit()
        return {"success", 200}
    except Exception as e:
        print('exception in enterGroup:', e)
        raise e

@server.post("/group/accept_user")
def acceptUser(request: Request, token: Annotated[str, Depends(oauth2Schema)], groupName: str = None, username: str = None):
    #Admin is accepting the request of user to enter to group
    currUser = getCurrentUser(token)
    
    group = (db.query(Group).filter(Group.name == groupName).all())[0]
    userGroup = (db.query(UserGroup).filter(UserGroup.groupId == group.id and UserGroup.user_id == currUser).all())[0]

    if userGroup.isAdmin == False:
        return {"error": "You are not the admin of this group"}

    username = request.args.get('username', type = str)
    user = (db.query(User).filter(User.username == username).all())[0]


    request = (db.query(Requestt).filter(Requestt.groupId == group.id and Requestt.senderId == user.id).all())[0]

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
    insert_stmt = insert(UserGroup).values(user_id=request.senderId, groupId=request.groupId, isAdmin=False)
    db.execute(insert_stmt)
    db.commit()
    #new_user_group = UserGroup(user_id=request.senderId, groupId=request.groupId, isAdmin=False)
    #db.add(new_user_group)
    
    # Delete the request
    #db.delete(request)
    delete_stmt = delete(Request).where(Request.groupId == request.groupId and Request.senderId == request.senderId)
    db.execute(delete_stmt)
    
    try:
        db.commit()
        return {"success", 200}
    except Exception as e:
        print('exception in acceptUser:', e)
        raise e

@server.delete("/group/leave_group")
def leaveGroup(request: Request, token: Annotated[str, Depends(oauth2Schema)], groupName: str = None):
    currUser = getCurrentUser(token)

    group = (db.query(Group).filter(Group.name == groupName).all())[0]

    #userGroup = UserGroup(currUser.id, group.id)
    #db.delete(userGroup)

    delete_stmt = delete(UserGroup).where(UserGroup.user_id == currUser.id and UserGroup.groupId == group.id)
    db.execute(delete_stmt)
    
    try:
        db.commit()
        return {"success", 200}
    except Exception as e:
        print('exception in leaveGroup:', e)
        raise e

@server.delete("/group/remove_group")
def removeGroup(request: Request, token: Annotated[str, Depends(oauth2Schema)], groupName: str = None):
    group = (db.query(Group).filter(Group.name == groupName).all())[0]

    # Delete references to the group in the UserGroup table
    #db.query(UserGroup).filter(UserGroup.groupId == group.id).delete()
    delete_stmt = delete(UserGroup).where(UserGroup.groupId == group.id)
    db.execute(delete_stmt)
    db.commit()
    
    # Delete the group itself
    #db.query(Group).filter(Group.id == group.id).delete()
    delete_stmt = delete(Group).where(Group.id == group.id)
    db.execute(delete_stmt)
    
    try:
        db.commit()
        return {"success", 200}
    except Exception as e:
        print('exception in removeGroup:', e)
        raise e
    
server.get("/group/addPassword")
def addPasswordToGroup(request: Request, token: Annotated[str, Depends(oauth2Schema)], groupName: str = None, password: str = None, name: str = None, shared: str = None):
    currUser = getCurrentUser(token)
    currGroup = (db.query(Group).filter(Group.name == groupName).all())[0]
    userGroup = (db.query(UserGroup).filter(UserGroup.user_id == currUser.id and UserGroup.groupId == currGroup.id).all())[0]
    if userGroup.isAdmin == False:
        return {"error": "You are not the admin of this group"}

    #db.add(Password(password, name, shared))
    insert_stmt = insert(Password).values(password=password, name=name, shared=shared)
    db.execute(insert_stmt)
    db.commit()
    password = (db.query(Password).filter(Password.password == password and Password.name == name and Password.shared == shared).all())[0]
    insert_stmt = insert(UserPassword).values(user_id=currUser.id, password_id=password.id)
    db.execute(insert_stmt)
    #db.add(UserPassword(currUser.id, password.id))
    
    try:
        db.commit()
        return {"success", 200}
    except Exception as e:
        print('exception in addPasswordToGroup:', e)
        raise e
    
@server.get("/group/removePassword")
def removePasswordFromGroup(request: Request, token: Annotated[str, Depends(oauth2Schema)], groupName: str = None, passwordId: int = None):
    currUser = getCurrentUser(token)
    currGroup = (db.query(Group).filter(Group.name == groupName).all())[0]
    userGroup = (db.query(UserGroup).filter(UserGroup.user_id == currUser.id and UserGroup.groupId == currGroup.id).all())[0]
    if userGroup.isAdmin == False:
        return {"error": "You are not the admin of this group"}

    #db.query(UserPassword).filter(UserPassword.passwordId == passwordId).delete()
    delete_stmt = delete(UserPassword).where(UserPassword.passwordId == passwordId)
    db.execute(delete_stmt)
    db.commit()

    delete_stmt = delete(Password).where(Password.id == passwordId)
    db.execute(delete_stmt)
    
    try:
        db.commit()
        return {"success", 200}
    except Exception as e:
        print('exception in removePasswordFromGroup:', e)
        raise e
    
@server.get("/group/updPassword")
def updatePasswordInGroup(request: Request, token: Annotated[str, Depends(oauth2Schema)], groupName: str = None, passwordId: int = None, newPassword: str = None, newName: str = None, shared: str = None):
    currUser = getCurrentUser(token)
    currGroup = (db.query(Group).filter(Group.name == groupName).all())[0]
    userGroup = (db.query(UserGroup).filter(UserGroup.user_id == currUser.id and UserGroup.groupId == currGroup.id).all())[0]
    if userGroup.isAdmin == False:
        return {"error": "You are not the admin of this group"}

    stmt = (
        update(Password)
        .where(Password.id == passwordId)
        .values(password=newPassword, name=newName, shared=shared)
    )
    db.execute(stmt)
    
    try:
        db.commit()
        return {"success", 200}
    except Exception as e:
        print('exception in updatePasswordInGroup:', e)
        raise e

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

@server.delete("/logout/")
def logout(request: Request, token: Annotated[str, Depends(oauth2Schema)]):
    currUser = getCurrentUser(token)

    #deleting all passwords of the user
    passwordsOfUser = (db.query(UserPassword).filter(UserPassword.user_id == currUser.id).all())
    for pw in passwordsOfUser:
        db.delete(pw)

    #deleting all groups of the user
    groupsOfUser = (db.query(UserGroup).filter(UserGroup.user_id == currUser.id).all())
    for group in groupsOfUser:
        db.delete(group)
    
    db.delete(currUser)

    try:
        db.commit()
        return {"success", 200}
    except Exception as e:
        print('exception in logout:', e)
        raise e

def getCurrentUser(token):
    # Get the username from the token
    #token = token.split(" ")[1]
    username = jwt.decode(token, "SARCASM", algorithms=["HS256"])["username"]
    print(username)

    return (db.query(User).filter(User.username == username).all())[0]

def getUsersOfGroup(group):
    usersInGroup = []
    # Get all users in the group
    usersId = db.query(UserGroup.user_id).filter(UserGroup.groupId == group.id).all()
    usersId = [u[0] for u in usersId]  # Extract user IDs
    for user_id in usersId:
        user = (db.query(User).filter(User.id == user_id).all())[0]#getting the user obj
        usersInGroup.append(user)

    return [{"id":user.id, "username": user.username, "email": user.email} for user in usersInGroup]

def getAllSharedPasswordsOfGroup(users):
    usersId = [u["id"]for u in users]

    # Get all shared passwords for these users
    shared_passwords = (db.query(Password).join(UserPassword, Password.id == UserPassword.passwordId).filter(UserPassword.user_id.in_(usersId), Password.shared == True).all())

    # Return the dict in list of shared passwords
    return [{"id": pw.id, "name": pw.name, "password": pw.password} for pw in shared_passwords]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(server, host="182.20.1.4", port=5001)