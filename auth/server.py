import datetime, os
from flask import Flask, request
from aes import AES
import database 

server = Flask(__name__)
aess = AES(b'\x00' * 16)

#config
server.config["HOST"] = "127.0.0.1"
server.config["AUTH_SVC_ADDRESS"] = '127.0.0.1:5000'
db = database.Database()

@server.route("/login", methods=["POST"])
def login():
    auth = request.authorization#getting the password and username
    if not auth:
        return "missing credentials", 401
    
    if db.doesUserExist(auth.username):
        if db.doesPasswordMatch(auth.username, auth.password):
            return createToken(auth.username, auth.password)
        else:
            return "invalid credentials", 401
    else:#if user isn't exist
        return "invalid credentials", 401
    
@server.route('/signup', methods=['POST'])
def signup():
    auth = request.authorization#getting the password and username
    if not auth:
        return "missing credentials", 401
    
    if db.doesUserExist(auth.username):
        return "invalid credentials", 401
    else:
        db.addUser(auth.username, auth.password, "shhhhhhh@")
        return createToken(auth.username, auth.password)

def createToken(username, password) -> str:
    stringForToken = username + password + "." + str(datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(days=1)) + "." + datetime.datetime.utcnow()
    return aess.encrypt_block(stringForToken.encode('utf-8'))

@server.route("/validate", methods=["POST"])
def validate():
    #this func is for the gateway, it would validate the token
    encodedToken = request.headers["Authorization"]

    if not encodedToken:#jwt is not present in Authorization header
        return "missing credentials", 401

    #Authorization: <type> <token>
    encodedToken = encodedToken.split(" ")[1]

    try:
        decoded = (aess.decrypt_block(encodedToken)).decode('utf-8')
    except:
        return "not authorized", 403

    return decoded, 200

if __name__ == "__main__":
    server.run(port=5000)