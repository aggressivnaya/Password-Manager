import os
from flask import Flask, request, jsonify
from sqlalchemy import update
import jwt
from common.base import session_factory, engine, Base
from groupsDb import Group
from historyDb import History
from request import Request
from usersDb import User
from passwordDb import Password
from usersGroups import UserGroup
from usersPasswordsDb import UserPassword

server = Flask(__name__)
server.config["DATA_SVC_ADDRESS"] = "182.20.1.4:5001"
db = session_factory()

'''
def validate(user):
    results = session_factory.query(User).filter(User.username == user.username).all()
    return results != None
    
@server.route("/login", methods=["GET"])
def login():
    username = request.args.get('username', type = str)
    #password = request.args.get('password')
    email = request.args.get('email', type = str)
    user = User(username, email)

    if email and not validate(user):
        db.add(user)
        db.commit()
        return "success!", 200
    elif not email and validate(username):
        return "success!", 200
    else:
        return "fail", 400
'''
    
@server.route("/changes", methods=["POST"])
def changes():
    func = request.args.get('func', type = str)
    currUser = getCurrentUser(request.headers["Authorization"].split(' ')[1])
    #username = request.args.get('username', type = str)
    
    #no need to check the username bc the username that we got in login
    #no need to check the passwords bc all the passwords are selected so 100% that is exist
    if func == 'add':
        password = request.args.get('password', type = str)
        name = request.args.get("name", type = str)
        shared = request.args.get("shared", type = str)
        password = Password(name, password, shared)
        return ("success", 200) if db.add(password) else ("faild to add", 400)
    elif func == 'update':
        currPasswordId = request.args.get('curr_password_id', type = int)
        newPassword = request.args.get('new_password', type = str)
        name = request.args.get("new_name", type = str)
        isShared = request.args.get("shared", type = str)

        #query that updates the password by id
        stmt = (
            update(Password)
            .where(Password.id == currPasswordId)
            .values(password=newPassword, name=name, shared=isShared)
        )

        db.execute(stmt)
        return ("success", 200) if db.commit() else ("faild to update", 400)
    elif func == 'delete':
        currPasswordId = request.args.get('curr_password_id', type = int)
        password = (db.query(Password).filter(Password.id == currPasswordId).all())[0]
        return ("success", 200) if db.delete(password) else ("faild to delete", 400)
    else:
        return "func is incorrect", 400
    
@server.route("/get", methods=["GET"])
def get():
    if request.args.get('password_id', default = -1, type = int) != -1:
        #finding the password by id
        passId = request.args.get('password_id', default = -1, type = int)
        password = (db.query(Password).filter(Password.id == passId).all())[0]
        return password, 200
    else:
        #finding by the user all his passwords
        #username = request.args.get('username', type = str)
        currUser = getCurrentUser(request.headers["Authorization"].split(' ')[1])

        passwords = (
            db.query(Password)
            .join(UserPassword, Password.id == UserPassword.passwordId)
            .filter(UserPassword.userId == currUser.id)
            .all()
        )

        # Return a list of password details
        return jsonify([{"id": password.id, "name": password.name, "password": password.password} for password in passwords]), 200
    
@server.route("/history", methods=["GET"])
def history():
    #tokenData = request.headers["Authorization"].split(' ')[1]
    #username = request.args.get('username', type = str)
    #user = (db.query(User).filter(User.username == username).all())[0]
    currUser = getCurrentUser(request.headers["Authorization"].split(' ')[1])

    result = (
        db.query(History)
        .join(Password, Password.id == History.passwordId)
        .join(UserPassword, UserPassword.passwordId == Password.id)
        .filter(UserPassword.userId == currUser.id)
        .all()
    )#lst of history objects

    return ("success", 200) if jsonify(result) else ("faild to get history", 400)

@server.route("/group/create_group", methods=["POST"])
def createGroup():
    #username = request.args.get('username', type = str)
    #user = (db.query(User).filter(User.username == username).all())[0]
    currUser = getCurrentUser(request.headers["Authorization"].split(' ')[1])

    #creating the group
    name = request.args.get('name', type = str)
    description = request.args.get('description')
    group = Group(name, description)
    db.add(group)
    db.commit()

    #adding the user to the group
    group = (db.query(Group).filter(Group.name == name and Group.description == description).all())[0]
    userGroup = UserGroup(currUser.id, group.id, True)
    db.add(userGroup)
    return ("success", 200) if db.commit() else ("faild to create room", 400)

@server.route("/group/enter_group", methods=["GET"])
def enterGroup():
    #sending request to admin user then waiting when admin accept
    #username = request.args.get('username', type = str)
    #user = (db.query(User).filter(User.username == username).all())[0]
    currUser = getCurrentUser(request.headers["Authorization"].split(' ')[1])

    groupName = request.args.get('group_name', type = str)
    group = (db.query(Group).filter(Group.name == groupName).all())[0]

    #finding the admin of the group
    userGroup = (db.query(UserGroup).filter(UserGroup.groupId == group.id and UserGroup.isAdmin == True).all())[0]
    request = Request(currUser.id, userGroup.userId, group.id)#creating an request to join to the group
    db.add(request)
    return ("success", 200) if db.commit() else ("faild to enter to group", 400)

@server.route("/group/accept_user", methods=["POST"])
def acceptUser():
    #admin is accepting the request of user to enter to group
    currUser = getCurrentUser(request.headers["Authorization"].split(' ')[1])
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
    
    return ("success", 200) if db.commit() else ("faild to accept user to group", 400)

@server.route("/group/leave_group", methods=["DELETE"])
def leaveGroup():
    #username = request.args.get('username', type = str)
    #user = (db.query(User).filter(User.username == username).all())[0]
    currUser = getCurrentUser(request.headers["Authorization"].split(' ')[1])

    groupName = request.args.get('group_name', type = str)
    group = (db.query(Group).filter(Group.name == groupName).all())[0]

    userGroup = UserGroup(currUser.id, group.id)
    db.delete(userGroup)
    return ("success", 200) if db.commit() else ("faild to leave room", 400)

@server.route("/group/remove_user", methods=["DELETE"])
def removeGroup():
    currUser = getCurrentUser(request.headers["Authorization"].split(' ')[1])
    #adminUsername = request.args.get('adminUsername', type = str)#TODO: you need to get this from the token
    groupName = request.args.get('group_name', type = str)
    group = (db.query(Group).filter(Group.name == groupName).all())[0]

    # Delete references to the group in the UserGroup table
    db.query(UserGroup).filter(UserGroup.groupId == group.id).delete()
    
    # Delete the group itself
    db.query(Group).filter(Group.id == group.id).delete()

    return ("success", 200) if db.commit() else ("faild to delete room", 400)

@server.route("/group", methods=["GET"])
def groupInfo():
    groupName = request.args.get("group_name", type = str)
    group = (db.query(Group).filter(Group.name == groupName).all())[0]
    #getting the users that in the group
    usersInGroup = getUsersOfGroup(group)

    #getting the passwords that in the group
    sharedPasswords = getAllSharedPasswordsOfGroup(usersInGroup)

    groupInfo = {"name": group.name, "description": group.description, "users": usersInGroup, "shared_passwords": sharedPasswords}
    
    if not groupInfo:
        return "error with group info", 400
    return groupInfo, 200

@server.route("/logout", methods=["DELETE"])
def logout():
    #loging out from the app complitely
    #username = request.args.get('username', type = str)
    #user = (db.query(User).filter(User.username == username).all())[0]
    currUser = getCurrentUser(request.headers["Authorization"].split(' ')[1])
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