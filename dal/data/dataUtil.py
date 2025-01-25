import os
from flask import Flask, request
import database as db
import userData 
import groupData
import passwordData
import requestData

server = Flask(__name__)
database = db.Database()
userDB = userData.User(database.conn, database.cursor)
requestDB = requestData.Request(database.conn, database.cursor)
groupDB = groupData.Group(database.conn, database.cursor)
passwordDB = passwordData.Password(database.conn, database.cursor)

server.config["DATA_SVC_ADDRESS"] = "182.20.1.4:5001"
#this is the only server that can communicate with database so others would only send query to this server and getting the response

def validate(username):
    #return database.doesUserExist(username)
    return userData.findId(username)
    
@server.route("/login", methods=["GET"])
def login():
    username = request.args.get('username')
    #password = request.args.get('password')
    email = request.args.get('email')

    if email and not validate(username):
        userData.add(username, email)
        return "success!", 200
    elif not email and validate(username):
        return "success!", 200
    else:
        return "fail", 400
    
@server.route("/changes", methods=["POST"])
def changes():
    func = request.form.get('func')
    username = request.form.get('username')
    #no need to check the username bc the username that we got in login
    #no need to check the passwords bc all the passwords are selected so 100% that is exist
    if func == 'add':
        password = request.form.get('password')
        name = request.form.get("name")
        shared = request.form.get("shared")
        return ("success", 200) if passwordDB.add(username, name, password,shared) else ("faild to add", 400)
    elif func == 'update':
        currPasswordId = request.form.get('curr_password_id')
        newPassword = request.form.get('new_password')
        name = request.form.get("new_name")
        isShared = request.form.get("shared")
        return ("success", 200) if passwordDB.update(username, currPasswordId, name, newPassword, isShared) else ("faild to update", 400)
    elif func == 'delete':
        currPasswordId = request.form.get('curr_password_id')
        return ("success", 200) if passwordDB.delete(username, currPasswordId) else ("faild to delete", 400)
    else:
        return "func is incorrect", 400
    
@server.route("/get", methods=["GET"])
def get():
    if request.args.get('password_id'):
        id = request.args.get('password_id')
        return passwordDB.findPassword(id), 200
    else:
        username = request.args.get('username')
        userId = userData.findId(username)
        return ("success", 200) if passwordDB.findId(userId) else ("faild to get password", 400)
    
@server.route("/history", methods=["GET"])
def history():
    username = request.args.get('username')
    userId = userData.findId(username)
    return ("success", 200) if passwordDB.getHistoryOfUser(userId) else ("faild to get history", 400)

@server.route("/group/create_group", methods=["POST"])
def createGroup():
    username = request.form.get('username')
    userId = userData.findId(username)
    name = request.form.get('name')
    description = request.form.get('description')
    return ("success", 200) if groupDB.create(userId, name, description) else ("faild to create room", 400)

@server.route("/group/enter_group", methods=["GET"])
def enterGroup():
    #sending request to admin user then waiting when admin accept
    username = request.args.get('username')
    groupId = request.args.get('group_id')
    return ("success", 200) if requestDB.add(username, groupId, "ENTER") else ("faild to enter to group", 400)

@server.route("/group/accept_user", methods=["POST"])
def acceptUser():
    adminUsername = request.form.get('adminUsername')
    username = request.form.get('username')
    groupId = request.form.get('group_id')
    return ("success", 200) if groupDB.accept(adminUsername, username, groupId) else ("faild to accept user to group", 400)

@server.route("/group/leave_group", methods=["DELETE"])
def leaveGroup():
    username = request.form.get('username')
    groupId = request.form.get('group_id')
    return ("success", 200) if groupDB.leave(username, groupId) else ("faild to leave room", 400)

@server.route("/group/remove_user", methods=["DELETE"])
def removeGroup():
    adminUsername = request.form.get('adminUsername')
    groupId = request.form.get('group_id')
    return ("success", 200) if groupDB.remove(adminUsername, groupId) else ("faild to create room", 400)

@server.route("/group", methods=["GET"])
def groupInfo():
    groupId = request.args.get("group_id")
    groupInfo = groupDB.getInfo(groupId)
    print(groupInfo)
    passwords = passwordDB.getSharedPasswords(groupId)
    print(passwords)
    if not groupInfo:
        return "error with group info", 400
    return groupInfo[0], 200

@server.route("/logout", methods=["DELETE"])
def logout():
    username = request.args.get('username')
    userId = userData.findId(username)
    return ("success", 200) if userData.logout(userId) else ("faild to logout", 400)

if __name__ == "__main__":
    #127.0.0.1
    #182.20.1.4
    server.run(host="127.0.0.1", port=5001)