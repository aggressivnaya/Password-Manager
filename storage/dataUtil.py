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

def validate(username, password):
    return database.doesUserExist(username) and database.doesPasswordMatch(username, password)
    
@server.route("/login", methods=["GET"])
def login():
    username = request.args.get('username')
    password = request.args.get('password')
    email = request.args.get('email')

    if email and not validate(username, password):
        database.addUser(username, password, email)
        return "success!", 200
    elif not email and validate(username,password):
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
        currPassword = request.form.get('curr_password')
        return "success", 200 if database.addPassword(username, currPassword)[1] == 200 else "faild to add", 400
    elif func == 'update':
        currPassword = request.form.get('curr_password_id')
        newPassword = request.form.get('new_password')
        return "success", 200 if database.updatePassword(username, currPassword, newPassword)[1] == 200 else "faild to update", 400
    elif func == 'delete':
        currPassword = request.form.get('curr_password')
        return "success", 200 if database.deletePassword(username, currPassword)[1] == 200 else "faild to delete", 400
    else:
        return "func is incorrect", 400
    
@server.route("/get", methods=["GET"])
def get():
    if request.args.get('password_id'):
        id = request.args.get('password_id')
        return database.findPasswordById(id), 200
    else:
        username = request.args.get('username')
        return database.getPasswords(username), 200
    
if __name__ == "__main__":
    server.run(port=5001)