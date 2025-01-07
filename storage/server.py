import os
from flask import Flask, request, jsonify
from sqlalchemy import update
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

def validate(user):
    results = session_factory.query(User).filter(User.username == user.username).all()
    return results != None
    
@server.route("/login", methods=["GET"])
def login():
    username = request.args.get('username')
    #password = request.args.get('password')
    email = request.args.get('email')
    user = User(username, email)

    if email and not validate(user):
        db.add(user)
        db.commit()
        return "success!", 200
    elif not email and validate(username):
        return "success!", 200
    else:
        return "fail", 400
    
@server.route("/changes", methods=["POST"])
def changes():
    func = request.form.get('func')
    username = request.form.get('username')
    user = User(username, "")
    #no need to check the username bc the username that we got in login
    #no need to check the passwords bc all the passwords are selected so 100% that is exist
    if func == 'add':
        password = request.form.get('password')
        name = request.form.get("name")
        shared = request.form.get("shared")
        password = Password(name, password, shared)
        return ("success", 200) if db.add(password) else ("faild to add", 400)
    elif func == 'update':
        currPasswordId = request.form.get('curr_password_id')
        newPassword = request.form.get('new_password')
        name = request.form.get("new_name")
        isShared = request.form.get("shared")
        stmt = (
            update(Password)
            .where(Password.id == currPasswordId)
            .values(password=newPassword, name=name, shared=isShared)
        )
        db.execute(stmt)
        return ("success", 200) if db.commit() else ("faild to update", 400)
    elif func == 'delete':
        currPasswordId = request.form.get('curr_password_id')
        password = (db.query(Password).filter(Password.id == currPasswordId).all())[0]
        return ("success", 200) if db.delete(password) else ("faild to delete", 400)
    else:
        return "func is incorrect", 400
    
@server.route("/get", methods=["GET"])
def get():
    if request.args.get('password_id'):
        #finding the password by id
        passId = request.args.get('password_id')
        password = (db.query(Password).filter(Password.id == passId).all())[0]
        return password, 200
    else:
        #finding by the user all his passwords
        username = request.args.get('username')
        user = (db.query(User).filter(User.username == username).all())[0]

        passwords = (
            db.query(Password)
            .join(UserPassword, Password.id == UserPassword.passwordId)
            .filter(UserPassword.userId == user.id)
            .all()
        )

        # Return a list of password details
        return jsonify([{"id": password.id, "name": password.name, "password": password.password} for password in passwords]), 200
    
@server.route("/history", methods=["GET"])
def history():
    username = request.args.get('username')
    user = (db.query(User).filter(User.username == username).all())[0]

    result = (
        db.query(History)
        .join(Password, Password.id == History.passwordId)
        .join(UserPassword, UserPassword.passwordId == Password.id)
        .filter(UserPassword.userId == user.id)
        .all()
    )#lst of history objects

    return ("success", 200) if jsonify(result) else ("faild to get history", 400)

@server.route("/group/create_group", methods=["POST"])
def createGroup():
    username = request.form.get('username')
    user = (db.query(User).filter(User.username == username).all())[0]

    #creating the group
    name = request.form.get('name')
    description = request.form.get('description')
    group = Group(name, description)
    db.add(group)
    db.commit()

    #adding the user to the group
    group = (db.query(Group).filter(Group.name == name and Group.description == description).all())[0]
    userGroup = UserGroup(user.id, group.id, True)
    db.add(userGroup)
    return ("success", 200) if db.commit() else ("faild to create room", 400)

@server.route("/group/enter_group", methods=["GET"])
def enterGroup():
    #sending request to admin user then waiting when admin accept
    username = request.args.get('username')
    user = (db.query(User).filter(User.username == username).all())[0]

    groupName = request.args.get('group_name')
    group = (db.query(Group).filter(Group.name == groupName).all())[0]

    userGroup = (db.query(UserGroup).filter(UserGroup.groupId == group.id and UserGroup.isAdmin == True).all())[0]
    request = Request(user.id, userGroup.userId, group.id)#creating an request to join to the group
    db.add(request)
    return ("success", 200) if db.commit() else ("faild to enter to group", 400)

@server.route("/group/accept_user", methods=["POST"])
def acceptUser():
    #admin is accepting the request of user to enter to group
    adminUsername = request.form.get('adminUsername')#TODO: check with token
    username = request.form.get('username')
    user = (db.query(User).filter(User.username == username).all())[0]

    groupName = request.form.get('group_name')
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
    username = request.form.get('username')
    user = (db.query(User).filter(User.username == username).all())[0]

    groupName = request.form.get('group_name')
    group = (db.query(Group).filter(Group.name == groupName).all())[0]

    userGroup = UserGroup(user.id, group.id)
    db.delete(userGroup)
    return ("success", 200) if db.commit() else ("faild to leave room", 400)

@server.route("/group/remove_user", methods=["DELETE"])
def removeGroup():
    adminUsername = request.form.get('adminUsername')#TODO: you need to get this from the token
    groupName = request.form.get('group_name')
    group = (db.query(Group).filter(Group.name == groupName).all())[0]

    # Delete references to the group in the UserGroup table
    db.query(UserGroup).filter(UserGroup.groupId == group.id).delete()
    
    # Delete the group itself
    db.query(Group).filter(Group.id == group.id).delete()

    return ("success", 200) if db.commit() else ("faild to delete room", 400)

@server.route("/group", methods=["GET"])
def groupInfo():
    groupName = request.args.get("group_name")
    group = (db.query(Group).filter(Group.name == groupName).all())[0]
    #getting the users that in the group
    usersInGroup = getUsersOfGroup(group)

    #getting the passwords that in the group
    sharedPasswords = getAllSharedPasswordsOfGroup(usersInGroup)

    groupInfo = {"name": group.name, "description": group.description, "users": usersInGroup, "shared_passwords": sharedPasswords}
    
    if not groupInfo:
        return "error with group info", 400
    return groupInfo, 200

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

@server.route("/logout", methods=["DELETE"])
def logout():
    #loging out from the app complitely
    username = request.args.get('username')
    user = (db.query(User).filter(User.username == username).all())[0]
    db.delete(user)
    return ("success", 200) if db.commit() else ("faild to logout", 400)

if __name__ == "__main__":
    #127.0.0.1
    #182.20.1.4
    server.run(host="127.0.0.1", port=5001)