import datetime, os,jwt
from flask import Flask, request
#import database 
from get_from_db import get

server = Flask(__name__)

#config
server.config["HOST"] = "127.0.0.1"
server.config["AUTH_SVC_ADDRESS"] = '127.0.0.1:5000'

@server.route("/login", methods=["POST"])
def login():
    auth = request.authorization#getting the password and username
    if not auth:
        return "missing credentials", 401
    
    if get.login(auth.username):
        return createToken(auth.username), 200
    else:
        return "invalid credentials", 401    
    
@server.route('/signup', methods=['POST'])
def signup():
    auth = request.authorization#getting the password and username
    if not auth:
        return "missing credentials", 401
    
    if get.signup(auth.username, auth.password):
        return createToken(auth.username), 200
    else:
        return "invalid credentials", 401

def createToken(username) -> str:
    return jwt.encode(
        {
            "username": username,
            "exp": datetime.datetime.now(tz=datetime.timezone.utc)
            + datetime.timedelta(days=1),
            "iat": datetime.datetime.utcnow(),
        },
        "SARCASM",
        algorithm="HS256",
    )

@server.route("/validate", methods=["POST"])
def validate():
    encoded_jwt = request.headers["Authorization"]

    if not encoded_jwt:
        return "missing credentials", 401

    try:
        decoded = jwt.decode(
            encoded_jwt, "SARCASM", algorithms=["HS256"]
        )

        if not get.login(decoded["username"]) and decoded["exp"] == decoded["iat"]:
            return "token is wrong", 400
    except:
        return "not authorized", 403

    return decoded, 200

    
if __name__ == "__main__":
    server.run(host="127.0.0.1", port=5000)