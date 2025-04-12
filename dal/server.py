import random
from fastapi import FastAPI, Header, Request, Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import update, insert, delete
from datetime import datetime
from typing import Annotated
import jwt
import os
import sys
import json
sys.path.append(os.path.abspath('..'))
from common.base import session_factory, engine, Base, _SessionFactory
from common.classes import User, Password, UserPassword, Group, UserGroup, Requestt, History

server = FastAPI()
#db = _SessionFactory()
session_factory()
server.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
oauth2Schema = OAuth2PasswordBearer(tokenUrl="placeholder")
    
@server.get("/user")
def getUser(request: Request, token: Annotated[str, Depends(oauth2Schema)]):
    db = _SessionFactory()
    currUser = getCurrentUser(token)
    print('currUser: ',currUser.username)

    return {'user': {"id": currUser.id, "username": currUser.username, "email": currUser.email}}

@server.post("/changes/add/")
def addPassword(request: Request, token: Annotated[str, Depends(oauth2Schema)], password: str = None, name: str = None, shared: str = None):
    db = _SessionFactory()
    currUser = getCurrentUser(token)
    print('adding password')
    if shared == "True":
        shared = True
    else:
        shared = False
    insert_stmt = insert(Password).values(name=name, password=password, shared=shared)
    db.execute(insert_stmt)
    db.commit()

    password = (db.query(Password).filter(Password.name == name and Password.password == password and Password.shared == shared).all())[0]
    insert_stmt = insert(UserPassword).values(userId=currUser.id, passwordId=password.id)
    db.execute(insert_stmt)
    db.commit()

    insert_stmt = insert(History).values(versionId=1, name=name, passwordId=password.id, method="add", date=datetime.utcnow().strftime("%Y-%m-%d"))
    db.execute(insert_stmt)

    try: 
        db.commit()
        db.close()
        return {"success": 200}
    except Exception as e:
        print('exception in addPassword:', e)
        raise e

@server.post("/changes/update/")
def updatePassword(request: Request, token: Annotated[str, Depends(oauth2Schema)], currPasswordId: int = None, newPassword: str = None, newName: str = None, shared: str = None):
    db = _SessionFactory()
    if shared == "True":
        shared = True
    else:
        shared = False
    #query that updates the password by id
    stmt = (
            update(Password)
            .where(Password.id == currPasswordId)
            .values(password=newPassword, name=newName, shared=shared)
        )

    db.execute(stmt)
    db.commit()

    insert_stmt = insert(History).values(versionId=1, name=newName, passwordId=currPasswordId, method="upd", date=datetime.utcnow().strftime("%Y-%m-%d"))
    db.execute(insert_stmt)

    try:
        db.commit()
        db.close()
        return {"success": 200}
    except Exception as e:
        print('exception in updatePassword:', e)
        raise e

@server.delete("/changes/delete/")
def deletePassword(request: Request, token: Annotated[str, Depends(oauth2Schema)], currPasswordId: int = None):
    db = _SessionFactory()
    currUser = getCurrentUser(token)
    password = (db.query(Password).filter(Password.id == currPasswordId).all())[0]

    delete_stmt = delete(Password).where(Password.id == currPasswordId)
    db.execute(delete_stmt)
    db.commit()
    delete_stmt = delete(UserPassword).where((UserPassword.passwordId == currPasswordId) & (UserPassword.userId == currUser.id))
    db.execute(delete_stmt)
    db.commit()

    insert_stmt = insert(History).values(versionId=1, name=password.name, passwordId=currPasswordId, method="del", date=datetime.utcnow().strftime("%Y-%m-%d"))
    db.execute(insert_stmt)

    try:
        db.commit()
        db.close()
        return {"success": 200}
    except Exception as e:
        print('exception in deletePassword:', e)
        raise e
    
@server.get("/getPassword")
def getRequiredPassword(passwordId: int = None):
    db = _SessionFactory()
    #finding the password by id
    print('passwordId: ',passwordId)
    print(db.query(Password).all())
    password = (db.query(Password).filter(Password.id == passwordId).all())[0]
    db.close()
    return {"password": password}

@server.get("/getPasswords")
def getUserPasswords(request: Request, token: Annotated[str, Depends(oauth2Schema)]):
    db = _SessionFactory()
    #finding by the user all his passwords
    print('token: ',token)
    currUser = getCurrentUser(token)
    print('currUser: ',currUser.username)

    passwords = (
        db.query(Password)
        .join(UserPassword, Password.id == UserPassword.passwordId)
        .filter(UserPassword.userId == currUser.id)
        .all()
    )
    print('password list: ',passwords)
    db.close()
    # Return a list of password details
    return {'passwords': [{"id": password.id, "name": password.name, "value": password.password, "shared": password.shared} for password in passwords]} 
    
@server.get("/history")
def history(request: Request, token: Annotated[str, Depends(oauth2Schema)]):
    db = _SessionFactory()
    currUser = getCurrentUser(token)

    result = (
        db.query(History)
        .join(Password, Password.id == History.passwordId)
        .join(UserPassword, UserPassword.passwordId == Password.id)
        .filter(UserPassword.userId == currUser.id)
        .all()
    )#lst of history objects
    db.close()
    if result:
        {"error":"faild to get history"}

    return {'history':result}

@server.get("/groups")
def getGroups(request: Request, token: Annotated[str, Depends(oauth2Schema)]):
    db = _SessionFactory()
    currUser = getCurrentUser(token)

    # Get all groups the user is in
    groups = (
        db.query(Group)
        .join(UserGroup, Group.id == UserGroup.groupId)
        .filter(UserGroup.userId == currUser.id)
        .all()
    )
    db.close()
    return {"groups": [group.name for group in groups]}

@server.post("/group/create_group")
def createGroup(request: Request, token: Annotated[str, Depends(oauth2Schema)], name: str = None, description: str = None):
    db = _SessionFactory()
    currUser = getCurrentUser(token)
    insert_stmt = insert(UserGroup).values(userId=currUser.id, groupId=3, isAdmin=True)
    db.execute(insert_stmt)
    db.commit()
    
    isGroup = (db.query(Group).filter(Group.name == name).all())
    if isGroup:
        return {"error": "Group already exists"}
    
    #creating the group
    link = name + str(random.randint(100000, 999999))
    insert_stmt = insert(Group).values(name=name, description=description, link=link)
    db.execute(insert_stmt)
    db.commit()
    #adding the user to the group
    group = (db.query(Group).filter(Group.name == name and Group.description == description).all())[0]
    print('group: ',group.id)
    insert_stmt = insert(UserGroup).values(userId=currUser.id, groupId=group.id, isAdmin=True)
    db.execute(insert_stmt)
    
    try:
        db.commit()
        db.close()
        return {"success": 200}
    except Exception as e:
        print('exception in createGroup:', e)
        raise e

@server.get("/group/enter_group")
def enterGroup(request: Request, token: Annotated[str, Depends(oauth2Schema)], groupLink: str = None):
    '''sending request to admin user then waiting when admin accept'''
    db = _SessionFactory()
    currUser = getCurrentUser(token)

    group = (db.query(Group).filter(Group.name == groupLink).all())[0]
    print('group: ',group.id)
    #finding the admin of the group
    userGroup = (db.query(UserGroup).filter((UserGroup.groupId == group.id) & (UserGroup.isAdmin == True)).all())[0]
    print('userGroup: ',userGroup)
    insert_stmt = insert(Requestt).values(sender_id=currUser.id, group_id=group.id,request_command="Join group")
    
    db.execute(insert_stmt)

    try:
        db.commit()
        db.close()
        return {"success": 200}
    except Exception as e:
        print('exception in enterGroup:', e)
        raise e
'''
@server.post("/group/accept_user")
def acceptUser(request: Request, token: Annotated[str, Depends(oauth2Schema)], groupName: str = None, username: str = None):
    db = _SessionFactory()
    #Admin is accepting the request of user to enter to group
    currUser = getCurrentUser(token)
    
    group = (db.query(Group).filter(Group.name == groupName).all())[0]
    userGroup = (db.query(UserGroup).filter(UserGroup.groupId == group.id and UserGroup.userId == currUser).all())[0]

    if userGroup.isAdmin == False:
        return {"error": "You are not the admin of this group"}

    print('username: ',username)
    user = (db.query(User).filter(User.username == username).all())[0]


    request = (db.query(Requestt).filter(Requestt.group_id == group.id and Requestt.sender_id == user.id).all())[0]

    # Find the manager of the group (isAdmin=True in UserGroup)
    manager = (
        db.query(UserGroup)
        .filter(UserGroup.groupId == request.group_id, UserGroup.isAdmin == True)
        .first()
    )
    if not manager:
        print(f"No manager found for group ID {request.group_id}.")
        return False
    
    # Add the user to the group
    insert_stmt = insert(UserGroup).values(userId=request.sender_id, groupId=request.group_id, isAdmin=False)
    db.execute(insert_stmt)
    db.commit()
    #new_user_group = UserGroup(user_id=request.senderId, groupId=request.groupId, isAdmin=False)
    #db.add(new_user_group)
    
    # Delete the request
    #db.delete(request)
    delete_stmt = delete(Requestt).where(Requestt.group_id == request.group_id and Requestt.sender_id == request.sender_id)
    db.execute(delete_stmt)
    
    try:
        db.commit()
        db.close()
        return {"success": 200}
    except Exception as e:
        print('exception in acceptUser:', e)
        raise e
        '''

@server.delete("/group/leave_group")
def leaveGroup(request: Request, token: Annotated[str, Depends(oauth2Schema)], groupName: str = None):
    db = _SessionFactory()
    currUser = getCurrentUser(token)

    group = (db.query(Group).filter(Group.name == groupName).all())[0]

    delete_stmt = delete(UserGroup).where(UserGroup.userId == currUser.id and UserGroup.groupId == group.id)
    db.execute(delete_stmt)
    
    try:
        db.commit()
        db.close()
        return {"success": 200}
    except Exception as e:
        print('exception in leaveGroup:', e)
        raise e

@server.delete("/group/remove_group")
def removeGroup(request: Request, token: Annotated[str, Depends(oauth2Schema)], groupName: str = None):
    db = _SessionFactory()
    group = (db.query(Group).filter(Group.name == groupName).all())[0]

    # Delete references to the group in the UserGroup table
    delete_stmt = delete(UserGroup).where(UserGroup.groupId == group.id)
    db.execute(delete_stmt)
    db.commit()
    
    # Delete the group itself
    delete_stmt = delete(Group).where(Group.id == group.id)
    db.execute(delete_stmt)
    
    try:
        db.commit()
        db.close()
        return {"success": 200}
    except Exception as e:
        print('exception in removeGroup:', e)
        raise e
'''   
@server.get("/group/addPassword")
def addPasswordToGroup(request: Request, token: Annotated[str, Depends(oauth2Schema)], groupName: str = None, password: str = None, name: str = None, shared: str = None):
    db = _SessionFactory()
    print('got the user')
    currUser = getCurrentUser(token)
    currGroup = (db.query(Group).filter(Group.name == groupName).all())[0]
    print('currGroup: ',currGroup)
    userGroup = (db.query(UserGroup).filter((UserGroup.userId == currUser.id) & (UserGroup.groupId == currGroup.id)).all())[0]
    print('userGroup: ',userGroup)
    if userGroup.isAdmin == False:
        return {"error": "You are not the admin of this group"}

    #db.add(Password(password, name, shared))
    if shared == "True":
        shared = True
    else:
        shared = False
    insert_stmt = insert(Password).values(password=password, name=name, shared=shared)
    db.execute(insert_stmt)
    db.commit()
    print('added password')
    password = (db.query(Password).filter(Password.password == password and Password.name == name and Password.shared == shared).all())[0]
    insert_stmt = insert(UserPassword).values(userId=currUser.id, passwordId=password.id)
    db.execute(insert_stmt)
    #db.add(UserPassword(currUser.id, password.id))
    print('added userpassword')
    try:
        db.commit()
        db.close()
        return {"success": 200}
    except Exception as e:
        print('exception in addPasswordToGroup:', e)
        raise e
    
@server.get("/group/removePassword")
def removePasswordFromGroup(request: Request, token: Annotated[str, Depends(oauth2Schema)], groupName: str = None, passwordId: int = None):
    db = _SessionFactory()
    currUser = getCurrentUser(token)
    currGroup = (db.query(Group).filter(Group.name == groupName).all())[0]
    userGroup = (db.query(UserGroup).filter(UserGroup.userId == currUser.id and UserGroup.groupId == currGroup.id).all())[0]
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
        db.close()
        return {"success": 200}
    except Exception as e:
        print('exception in removePasswordFromGroup:', e)
        raise e
    
@server.get("/group/updPassword")
def updatePasswordInGroup(request: Request, token: Annotated[str, Depends(oauth2Schema)], groupName: str = None, passwordId: int = None, newPassword: str = None, newName: str = None, shared: str = None):
    db = _SessionFactory()
    currUser = getCurrentUser(token)
    currGroup = (db.query(Group).filter(Group.name == groupName).all())[0]
    userGroup = (db.query(UserGroup).filter(UserGroup.userId == currUser.id and UserGroup.groupId == currGroup.id).all())[0]
    if userGroup.isAdmin == False:
        return {"error": "You are not the admin of this group"}

    if shared == "True":
        shared = True
    else:
        shared = False
    stmt = (
        update(Password)
        .where(Password.id == passwordId)
        .values(password=newPassword, name=newName, shared=shared)
    )
    db.execute(stmt)
    
    try:
        db.commit()
        db.close()
        return {"success": 200}
    except Exception as e:
        print('exception in updatePasswordInGroup:', e)
        raise e'''

@server.get("/group")
def groupInfo(groupName: str = None):
    db = _SessionFactory()
    group = (db.query(Group).filter(Group.name == groupName).all())[0]
    #getting the users that in the group
    usersInGroup = getUsersOfGroup(group)

    #getting the passwords that in the group
    sharedPasswords = getAllSharedPasswordsOfGroup(usersInGroup, group)

    groupInfo = {"name": group.name, "description": group.description, "users": usersInGroup, "sharedPasswords": sharedPasswords}
    db.close()
    if not groupInfo:
        return {"error": "error with group info"}
    return {'groupinfo':groupInfo}

@server.get("/group/requests")
def getRequests(request: Request, token: Annotated[str, Depends(oauth2Schema)], groupName: str = None):
    db = _SessionFactory()
    currUser = getCurrentUser(token)
    currGroup = (db.query(Group).filter(Group.name == groupName).all())[0]
    userGroup = (db.query(UserGroup).filter(UserGroup.userId == currUser.id and UserGroup.groupId == currGroup.id).all())[0]
    if userGroup.isAdmin == False:
        return {"error": "You are not the admin of this group"}
    
    #getting the requests of the group
    requests = (db.query(Requestt).filter(Requestt.group_id == currGroup.id).all())
    print('requests: ',requests)
    db.close()
    if not requests:
        return {"error": "error with group info"}
    return {'requests':requests}

@server.post("/group/approve_request")
def approveRequest(request: Request, token: Annotated[str, Depends(oauth2Schema)], groupName: str = None, requestId: int = None):
    db = _SessionFactory()
    currUser = getCurrentUser(token)
    currGroup = (db.query(Group).filter(Group.name == groupName).all())[0]
    userGroup = (db.query(UserGroup).filter(UserGroup.userId == currUser.id and UserGroup.groupId == currGroup.id).all())[0]
    if userGroup.isAdmin == False:
        return {"error": "You are not the admin of this group"}
    
    #finding the request by id
    request = (db.query(Requestt).filter(Requestt.id == requestId).all())[0]

    if request.request_command[0:3] == "ent":
        insert_stmt = insert(UserGroup).values(userId=request.sender_id, groupId=request.group_id, isAdmin=False)
        db.execute(insert_stmt)
        db.commit()
    elif request.request_command[0:3] == "add":
        #adding the password to the group
        print("in add function")
        print(request.request_command[3:])
        valid_json_str = request.request_command[3:].replace("'", '"')
        parsed = json.loads(valid_json_str)
        shared = parsed["shared"]
        if parsed["shared"] == "True":
            shared = True
        else:
            shared = False
        insert_stmt = insert(Password).values(password=parsed["password"], name=parsed["name"], shared=shared)
        db.execute(insert_stmt)
        db.commit()
        print('added password')
        password = (db.query(Password).filter(Password.password == parsed["password"] and Password.name == parsed["name"] and Password.shared == shared).all())[0]
        insert_stmt = insert(UserPassword).values(userId=currUser.id, passwordId=password.id)
        db.execute(insert_stmt)
        db.execute(insert_stmt)
        db.commit()
    elif request.request_command[0:3] == "del":
        #deleting the password from the group
        valid_json_str = request.request_command[3:].replace("'", '"')
        parsed = json.loads(valid_json_str)
        password = (db.query(Password).filter(Password.id == parsed["id"]).all())[0]
        delete_stmt = delete(UserPassword).where((UserPassword.passwordId == password.id) & (UserPassword.userId == request.sender_id))
        db.execute(delete_stmt)
        db.commit()
    elif request.request_command[0:3] == "upd":
        #updating the password in the group
        valid_json_str = request.request_command[3:].replace("'", '"')
        parsed = json.loads(valid_json_str)
        stmt = (
            update(Password)
            .where(Password.id == parsed["id"])
            .values(password=parsed["newPassword"], name=parsed["name"], shared=shared)
        )
        db.execute(stmt)
        db.commit()
    
    #deleting the request
    delete_stmt = delete(Requestt).where(Requestt.id == requestId)
    db.execute(delete_stmt)

    try:
        db.commit()
        db.close()
        return {"success": 200}
    except Exception as e:
        print('exception in approveRequest:', e)
        raise e
    
@server.delete("/group/deny_request")
def denyRequest(request: Request, token: Annotated[str, Depends(oauth2Schema)], groupName: str = None, requestId: int = None):
    db = _SessionFactory()
    currUser = getCurrentUser(token)
    currGroup = (db.query(Group).filter(Group.name == groupName).all())[0]
    userGroup = (db.query(UserGroup).filter(UserGroup.userId == currUser.id and UserGroup.groupId == currGroup.id).all())[0]
    if userGroup.isAdmin == False:
        return {"error": "You are not the admin of this group"}
    
    #finding the request by id
    request = (db.query(Requestt).filter(Requestt.id == int(requestId)).all())[0]

    #deleting the request
    delete_stmt = delete(Requestt).where(Requestt.id == int(requestId))
    db.execute(delete_stmt)

    try:
        db.commit()
        db.close()
        return {"success": 200}
    except Exception as e:
        print('exception in denyRequest:', e)
        raise e

@server.post("/group/insert_request")
def insertRequest(request: Request, token: Annotated[str, Depends(oauth2Schema)], groupName: str = None, requestCommand: str = None):
    db = _SessionFactory()
    currUser = getCurrentUser(token)
    currGroup = (db.query(Group).filter(Group.name == groupName).all())[0]
    
    #creating the request
    insert_stmt = insert(Requestt).values(sender_id=currUser.id, group_id=currGroup.id, request_command=requestCommand)
    db.execute(insert_stmt)

    try:
        db.commit()
        db.close()
        return {"success": 200}
    except Exception as e:
        print('exception in insertRequest:', e)
        raise e

@server.delete("/logout/")
def logout(request: Request, token: Annotated[str, Depends(oauth2Schema)]):
    db = _SessionFactory()
    currUser = getCurrentUser(token)

    #deleting all passwords of the user
    passwordsOfUser = (db.query(UserPassword).filter(UserPassword.userId == currUser.id).all())
    for pw in passwordsOfUser:
        db.delete(pw)

    #deleting all groups of the user
    groupsOfUser = (db.query(UserGroup).filter(UserGroup.userId == currUser.id).all())
    for group in groupsOfUser:
        db.delete(group)
    
    db.delete(currUser)

    try:
        db.commit()
        db.close()
        return {"success": 200}
    except Exception as e:
        print('exception in logout:', e)
        raise e

def getCurrentUser(token):
    # Get the username from the token
    db = _SessionFactory()
    print('token: ',token)
    username = jwt.decode(token, "SARCASM", algorithms=["HS256"])["username"]
    print('username: ',username)

    return (db.query(User).filter(User.username == username).all())[0]

def getUsersOfGroup(group):
    db = _SessionFactory()
    usersInGroup = []
    # Get all users in the group
    userss = db.query(UserGroup).filter(UserGroup.groupId == group.id).all()
    for i in userss:
        print('userId: ',i.userId)
        print('isAdmin: ',i.isAdmin)
    users = [(u.userId, u.isAdmin) for u in userss]  # Extract user IDs and isAdmin status
    print(users)
    for user in users:
        userFromDb = (db.query(User).filter(User.id == user[0]).all())[0]
        usersInGroup.append((userFromDb, user[1]))#user[1] is the isAdmin status
    db.close()
    
    print('usersInGroup: ',usersInGroup)
    return [{"id":user[0].id, "username": user[0].username, "email": user[0].email, "isAdmin": user[1]} for user in usersInGroup]

def getAllSharedPasswordsOfGroup(users, group):
    db = _SessionFactory()
    shared_passwords = (
        db.query(Password)
        .join(UserPassword, Password.id == UserPassword.passwordId)
        .join(UserGroup, UserPassword.userId == UserGroup.userId)
        .filter(UserGroup.groupId == group.id, Password.shared == True)
        .distinct()
        .all()
    )

    return [{"name": p.name, "password": p.password} for p in shared_passwords]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(server, host="182.20.1.4", port=5001)
    #uvicorn.run(server, host="127.0.0.1", port=5001)