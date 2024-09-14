import datetime, os
from flask import Flask, request
from aes import AES
#import database 
from get_from_db import get

server = Flask(__name__)
aess = AES(b'\x00' * 16)

#config
server.config["HOST"] = "127.0.0.1"
server.config["AUTH_SVC_ADDRESS"] = '127.0.0.1:5000'

@server.route("/login", methods=["POST"])
def login():
    auth = request.authorization#getting the password and username
    if not auth:
        return "missing credentials", 401
    
    if get.login(auth.username, auth.password):
        return createToken(auth.username, auth.password), 200
    else:
        return "invalid credentials", 401    
    
@server.route('/signup', methods=['POST'])
def signup():
    auth = request.authorization#getting the password and username
    if not auth:
        return "missing credentials", 401
    
    if get.signup(auth.username, auth.password):
        return createToken(auth.username, auth.password), 200
    else:
        return "invalid credentials", 401

def createToken(username, email) -> str:
    stringForToken = username + "." + email + "." + str(datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(days=1)) + "." + datetime.datetime.utcnow()
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
        info = decoded.split('.')
        #check if username exist
        if info[2] == info[3] and not get.login(info[0], info[1]):
            return 'error the token is expiered', 400
        else:
            return decoded, 200
    except:
        return "not authorized", 403

    
if __name__ == "__main__":
    server.run(port=5000)