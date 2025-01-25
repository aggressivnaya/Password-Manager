import datetime, os, jwt, random
from flask import Flask, request
from dal.usersDb import User
from common.base import session_factory
from send_noti import notification

server = Flask(__name__)
db = session_factory()

#config
#server.config["HOST"] = "182.20.1.3"
server.config["AUTH_SVC_ADDRESS"] = '182.20.1.3:5000'

@server.route("/login", methods=["POST"])
def login():
    auth = request.authorization#getting the password and username
    if not auth:
        return "missing credentials", 401
    
    genaretedCode = str(random.randint(100000, 999999))

    findingUser = (db.query(User).filter(User.username == auth.username and User.email == auth.password).all())[0]
    if findingUser != None and notification.sendEmail(auth.username, genaretedCode):
        return createToken(auth.username), 200
    else:
        return "invalid credentials", 401    
    
@server.route('/signup', methods=['POST'])
def signup():
    auth = request.authorization#getting the password and username
    if not auth:
        return "missing credentials", 401
    
    if db.add(User(auth.username, auth.password)):
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
    encoded_jwt = encoded_jwt.split(" ")[1]

    if not encoded_jwt:
        return "missing credentials", 401

    try:
        decoded = jwt.decode(
            encoded_jwt, "SARCASM", algorithms=["HS256"]
        )

        findingUser = (db.query(User).filter(User.username == decoded["username"]).all())[0]
        if not findingUser and decoded["exp"] == decoded["iat"]:
            return "token is wrong", 400

    except:
        return "not authorized", 403

    return decoded, 200
    
if __name__ == "__main__":
    server.run(host="182.20.1.3", port=5000)
