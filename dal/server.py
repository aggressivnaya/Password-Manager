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
from cryptography.fernet import Fernet
sys.path.append(os.path.abspath('..'))
from common.base import session_factory, engine, Base, _SessionFactory
from common.classes import User, Password, UserPassword, Group, UserGroup, Requestt, History, PasswordKey, Notification

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

    return {'user': {"id": currUser.id, "username": currUser.username, "email": currUser.email}}

@server.post("/changes/add/")
def addPassword(request: Request, token: Annotated[str, Depends(oauth2Schema)], password: str = None, name: str = None, shared: str = None):
    #generating the key and encrypting the password
    key = Fernet.generate_key()
    cipher = Fernet(key)
    db = _SessionFactory()
    currUser = getCurrentUser(token)

    #inserting the password to the db(Password table)
    sharedd = True if shared == "True" else False
    insert_stmt = insert(Password).values(name=name, password=cipher.encrypt(password.encode()), shared=sharedd)
    db.execute(insert_stmt)
    db.commit()

    #inserting the password to the db(UserPassword table)
    password = (db.query(Password).filter(Password.name == name and Password.password == cipher.encrypt(password.encode()) and Password.shared == shared).all())[0]
    insert_stmt = insert(UserPassword).values(userId=currUser.id, passwordId=password.id)
    db.execute(insert_stmt)
    db.commit()

    #inserting the password to the db(History table)
    insert_stmt = insert(History).values(versionId=1, name=name, passwordId=password.id, method="add", date=datetime.utcnow().strftime("%Y-%m-%d"))
    db.execute(insert_stmt)
    db.commit()

    #inserting the password to the db(PasswordKey table)
    insert_stmt = insert(PasswordKey).values(passwordId=password.id, key=key)
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
    #updating the password in the db
    sharedd = True if shared == "True" else False
    #currPassword = (db.query(Password).filter(Password.id == currPasswordId).all())[0]
    key = (db.query(PasswordKey).filter(PasswordKey.passwordId == currPasswordId).all())[0]
    cipher = Fernet(key.key)
    stmt = (
            update(Password)
            .where(Password.id == currPasswordId)#query that updates the password by id
            .values(password=cipher.encrypt(newPassword.encode()), name=newName, shared=sharedd)
        )

    db.execute(stmt)
    db.commit()

    #inserting the password to the db(History table)
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
    password = (db.query(Password).filter(Password.id == currPasswordId).all())
    if len(password) == 0:
        return {"error": "Password not found"}
    password = password[0]

    #deleting the password from the db(Password table)
    delete_stmt = delete(Password).where(Password.id == currPasswordId)
    db.execute(delete_stmt)
    db.commit()

    #deleting the password from the db(UserPassword table)
    delete_stmt = delete(UserPassword).where((UserPassword.passwordId == currPasswordId) & (UserPassword.userId == currUser.id))
    db.execute(delete_stmt)
    db.commit()

    #deleting the password from the db(PasswordKey table)
    delete_stmt = delete(PasswordKey).where(PasswordKey.passwordId == currPasswordId)
    db.execute(delete_stmt)
    db.commit()

    #inserting the password to the db(History table)
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
    password = (db.query(Password).filter(Password.id == passwordId).all())[0]
    key = (db.query(PasswordKey).filter(PasswordKey.passwordId == passwordId).all())
    if len(key) == 0:
        return {"password": password}
    cipher = Fernet(key[0].key)
    password.password = cipher.decrypt(password.password).decode()
    db.close()
    return {"password": password}

@server.get("/getPasswords")
def getUserPasswords(request: Request, token: Annotated[str, Depends(oauth2Schema)]):
    db = _SessionFactory()
    #finding by the user all his passwords
    currUser = getCurrentUser(token)

    passwords = (
        db.query(Password)
        .join(UserPassword, Password.id == UserPassword.passwordId)
        .filter(UserPassword.userId == currUser.id)
        .all()
    )

    # Decrypt the passwords
    for password in passwords:
        print("password: ",password.password, "id: ",password.id)
        key = (db.query(PasswordKey).filter(PasswordKey.passwordId == int(password.id)).all())
        print(key)
        if len(key) == 0:
            continue
        cipher = Fernet(key[0].key)
        password.password = cipher.decrypt(password.password).decode()
    db.close()
    for p in passwords:
        print("password: ",p.password, "shared: ",p.shared)
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

    historyMsg = []
    for history in result:
        # Decrypt the passwords
        password = (db.query(Password).filter(Password.name == history.name).all())[0]
        key = (db.query(PasswordKey).filter(PasswordKey.passwordId == int(password.id)).all())
        if len(key) == 0:
            continue
        cipher = Fernet(key[0].key)
        try:
            password.password = cipher.decrypt(password.password).decode()
        except Exception as e:
            continue
        historyMsg.append({"id": history.id, "name": history.name,"password": password.password, "method": history.method, "date": history.date})
    # Return a list of password details
    return {'history': historyMsg}

@server.get("/notifications")
def getNotifications(request: Request, token: Annotated[str, Depends(oauth2Schema)]):
    db = _SessionFactory()
    currUser = getCurrentUser(token)

    # Get all notifications for the current user
    notifications = (
        db.query(Notification)
        .filter(Notification.sender_id == currUser.id or Notification.reciever_id == currUser.id)
        .all()
    )
    db.close()

    notificationsMsg = []
    for notification in notifications:
        notificationsMsg.append({"id": notification.id, "sender_id": notification.sender_id, "reciever_id": notification.reciever_id, "data": notification.data})
    
    return {'notifications': notificationsMsg}

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
    #finding the admin of the group
    userGroup = (db.query(UserGroup).filter((UserGroup.groupId == group.id) & (UserGroup.isAdmin == True)).all())[0]
    #sending request to the admin of the group(inserting to the Request table)
    insert_stmt = insert(Requestt).values(sender_id=currUser.id, group_id=group.id,request_command="Join group")
    
    db.execute(insert_stmt)

    try:
        db.commit()
        db.close()
        return {"success": 200}
    except Exception as e:
        print('exception in enterGroup:', e)
        raise e

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

@server.get("/group")
def groupInfo(groupName: str = None):
    db = _SessionFactory()
    group = (db.query(Group).filter(Group.name == groupName).all())[0]
    #getting the users that in the group
    usersInGroup = getUsersOfGroup(group)
    #getting the passwords that in the group
    sharedPasswords = getAllSharedPasswordsOfGroup(usersInGroup, group)
    print('sharedPasswords: ',sharedPasswords)

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
    requestsMsg = []
    for r in requests:
        requestsMsg.append({"id": r.id, "sender_id": r.sender_id, "request_command": r.request_command})
    db.close()

    if not requestsMsg:
        return {"error": "error with group info"}
    return {'requests':requestsMsg}

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
        addUserToGroup(request.sender_id, request.group_id)
    elif request.request_command[0:3] == "add":
        addPasswordToGroup(request.request_command[3:], request.sender_id)
    elif request.request_command[0:3] == "del":
        deletePasswordFromGroup(request.request_command[3:], request.sender_id)
    elif request.request_command[0:3] == "upd":
        updatePasswordInGroup(request.request_command[3:])
    
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
    
    #deleting the request(from the Request table)
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
    
    #creating the request and inserting it to the db(Request table)
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
    username = jwt.decode(token, "SARCASM", algorithms=["HS256"])["username"]

    return (db.query(User).filter(User.username == username).all())[0]

def getUsersOfGroup(group):
    db = _SessionFactory()
    usersInGroup = []
    # Get all users in the group
    userss = db.query(UserGroup).filter(UserGroup.groupId == group.id).all()
    users = [(u.userId, u.isAdmin) for u in userss]  # Extract user IDs and isAdmin status
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
    # Decrypt the passwords
    for password in shared_passwords:
        key = (db.query(PasswordKey).filter(PasswordKey.passwordId == password.id).all())[0]
        cipher = Fernet(key.key)
        password.password = cipher.decrypt(password.password).decode()
    db.close()

    return [{"id": p.id,"name": p.name, "password": p.password} for p in shared_passwords]

def addUserToGroup(userId, groupId):
    db = _SessionFactory()
    insert_stmt = insert(UserGroup).values(userId=userId, groupId=groupId, isAdmin=False)
    db.execute(insert_stmt)
    db.commit()
    db.close()

def addPasswordToGroup(jsonOfPassword, userId):
    db = _SessionFactory()
    #adding the password to the group
    key = Fernet.generate_key()
    cipher = Fernet(key)
    valid_json_str = jsonOfPassword.replace("'", '"')
    parsed = json.loads(valid_json_str)
    shared = parsed["shared"]
    #inserting the password to the db(Password table)
    shared = "True" if shared else "False"
    insert_stmt = insert(Password).values(password=cipher.encrypt(parsed["password"].encode()), name=parsed["name"], shared=shared)
    db.execute(insert_stmt)
    db.commit()

    #inserting the password to the db(PasswordKey table)
    insert_stmt = insert(PasswordKey).values(passwordId=parsed["id"], key=key)
    db.execute(insert_stmt)
    db.commit()

    password = (db.query(Password).filter(Password.password == parsed["password"] and Password.name == parsed["name"] and Password.shared == shared).all())[0]
    insert_stmt = insert(UserPassword).values(userId=userId, passwordId=password.id)
    db.execute(insert_stmt)
    db.commit()
    db.close()

def deletePasswordFromGroup(jsonOfPassword, userId):
    db = _SessionFactory()
    #deleting the password from the group
    valid_json_str = jsonOfPassword.replace("'", '"')
    parsed = json.loads(valid_json_str)
    password = (db.query(Password).filter(Password.id == parsed["id"]).all())[0]
    delete_stmt = delete(UserPassword).where((UserPassword.passwordId == password.id) & (UserPassword.userId == userId))
    db.execute(delete_stmt)
    db.commit()
    db.close()

def updatePasswordInGroup(jsonOfPassword):
    db = _SessionFactory()
    #updating the password in the group
    valid_json_str = jsonOfPassword.replace("'", '"')
    print('valid_json_str: ',valid_json_str)
    parsed = json.loads(valid_json_str)
    if parsed["shared"] == "True":
        shared = True
    else:
        shared = False
    currPassword = (db.query(Password).filter(Password.id == parsed["id"]).all())[0]
    key = (db.query(PasswordKey).filter(PasswordKey.passwordId == currPassword.id).all())[0]
    cipher = Fernet(key.key)
    stmt = (
        update(Password)
        .where(Password.id == parsed["id"])
        .values(password=cipher.encrypt(parsed["newPassword"].encode()), name=parsed["name"], shared=shared)
    )
    db.execute(stmt)
    db.commit()
    db.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(server, host="182.20.1.4", port=5001)
    #uvicorn.run(server, host="127.0.0.1", port=5001)