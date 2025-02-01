import datetime, os, jwt, random
#from flask import Flask, request
from fastapi import FastAPI, Header
from dal.classes.usersDb import User
from common.base import session_factory
from send_noti import notification

server = FastAPI()
db = session_factory()

#config
#server.config["HOST"] = "182.20.1.3"
#server.config["AUTH_SVC_ADDRESS"] = '182.20.1.3:5000'

@server.post("/login/")
def login(name: str, email: str):
    genaretedCode = str(random.randint(100000, 999999))

    findingUser = (db.query(User).filter(User.username == name and User.email == email).all())[0]
    if findingUser != None and notification.sendEmail(name, genaretedCode):
        return {"token": createToken(name)}
    else:
        return {"error": "invalid credentials"}
    
@server.post('/signup/')
def signup(name: str, email: str):
    if db.add(User(name, email)):
        return {"token": createToken(name)}
    else:
        return {"error": "invalid credentials"}

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

@server.post("/validate/")
def validate(authorization: str = Header(None)):
    if not authorization:
        return {"error": "missing credentials"}

    encoded_jwt = authorization.split(" ")[1]

    try:
        decoded = jwt.decode(
            encoded_jwt, "SARCASM", algorithms=["HS256"]
        )

        findingUser = (db.query(User).filter(User.username == decoded["username"]).all())[0]
        if not findingUser and decoded["exp"] == decoded["iat"]:
            return {"error": "token is wrong"}

    except:
        return {"error": "not authorized"}

    return {"decoded": decoded}
    
if __name__ == "__main__":
    server.run(host="182.20.1.3", port=5000)
