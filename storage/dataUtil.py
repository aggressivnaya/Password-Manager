import os
from flask import Flask, request
import database as db

server = Flask(__name__)
database = db.Database()

server.config["DATA_SVC_ADDRESS"] = "127.0.0.1:5001"
#this is the only server that can communicate with database so others would only send query to this server and getting the response
#querys that server could get:
#check valide user(if user exist and password match(password by default can be empty then we know that we need to check only if user exist)) -> return true or false
#add user
#add password
#get passwords
#get curr password
#update password
#delete password

def validate(username):
    #return database.doesUserExist(username)
    return database.findUserIdByUsername(username)
    
@server.route("/login", methods=["GET"])
def login():
    username = request.args.get('username')
    #password = request.args.get('password')
    email = request.args.get('email')

    if email and not validate(username):
        database.addUser(username, email)
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
        return ("success", 200) if database.addPassword(username, name, password,shared) else ("faild to add", 400)
    elif func == 'update':
        currPasswordId = request.form.get('curr_password_id')
        newPassword = request.form.get('new_password')
        name = request.form.get("new_name")
        isShared = request.form.get("shared")
        return ("success", 200) if database.updatePassword(username, currPasswordId, name, newPassword, isShared) else ("faild to update", 400)
    elif func == 'delete':
        currPasswordId = request.form.get('curr_password_id')
        return ("success", 200) if database.deletePassword(username, currPasswordId) else ("faild to delete", 400)
    else:
        return "func is incorrect", 400
    
@server.route("/get", methods=["GET"])
def get():
    if request.args.get('password_id'):
        id = request.args.get('password_id')
        return database.findPasswordById(id), 200
    else:
        username = request.args.get('username')
        userId = database.findUserIdByUsername(username)
        return ("success", 200) if database.getPasswordsForUser(userId) else ("faild to get password", 400)
    
@server.route("/history", methods=["GET"])
def history():
    username = request.args.get('username')
    userId = database.findUserIdByUsername(username)
    return ("success", 200) if database.getHistoryOfUser(userId) else ("faild to get history", 400)

@server.route("/group/create", methods=["POST"])
def createGroup():
    username = request.form.get('username')
    userId = database.findUserIdByUsername(username)
    name = request.form.get('name')
    description = request.form.get('description')
    return ("success", 200) if database.createGroup(userId, name, description) else ("faild to create room", 400)

@server.route("/group/accept_user", methods=["POST"])
def acceptUser():
    pass

@server.route("/group/leave_group", methods=["DELETE"])
def leaveGroup():
    pass

@server.route("/gorup/remove_user", methods=["DELETE"])
def removeGroup():
    pass

@server.route("/group", methods=["GET"])
def groupInfo():
    groupId = request.args.get("group_id")
    groupInfo = database.getGroupInfo(groupId)
    passwords = database.getSharedPasswords(groupId)
    return groupInfo, passwords

@server.route("/logout", methods=["DELETE"])
def logout():
    username = request.args.get('username')
    userId = database.findUserIdByUsername(username)
    return ("success", 200) if database.logoutFromServer(userId) else ("faild to logout", 400)

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=5001)