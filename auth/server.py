import datetime, os, jwt, random
from pydantic import BaseModel
#from flask import Flask, request
from fastapi import FastAPI, Header, Request, HTTPException
import os
import sys
sys.path.append(os.path.abspath('..'))
#from dal.classes.usersDb import User
from common.classes import User
from common.base import session_factory
from send_noti import notification

server = FastAPI()
db = session_factory()

genaretedCode = ''

class User(BaseModel):
    name: str
    email: str

@server.post("/login/")
def login(user: User):
    global genaretedCode
    genaretedCode = str(random.randint(100000, 999999))

    findingUser = (db.query(User).filter(User.username == user.name and User.email == user.email).all())[0]
    if findingUser != None and notification.sendEmail(user.name, genaretedCode):
        return {"token": createToken(user.name)}
    else:
        return {"error": "invalid credentials"}
    
@server.get('/check')
def checkCode(code: str):
    if code == genaretedCode:
        return {'success': True}
    else:
        return {"error": "invalid code"}
    
@server.post('/signup/')
def signup(user: User):
    findingUser = (db.query(User).filter(User.username == user.name and User.email == user.email).all())[0]
    if findingUser == None and notification.sendEmail(user.name, genaretedCode):
        db.add(User(user.name, user.email))
        return {"token": createToken(user.name)}
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
def validate(request: Request):
    if not request.headers.get("Authorization"):
        raise HTTPException(status_code=401, detail="not authorized")

    encoded_jwt = request.headers.get("Authorization").split(" ")[1]

    try:
        decoded = jwt.decode(
            encoded_jwt, "SARCASM", algorithms=["HS256"]
        )

        findingUser = (db.query(User).filter(User.username == decoded["username"]).all())[0]
        if not findingUser and decoded["exp"] == decoded["iat"]:
            raise HTTPException(status_code=401, detail="not authorized")

    except:
        raise HTTPException(status_code=401, detail="not authorized")

    return {"validated": True}
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(server, host="182.20.1.3", port=5000)
    
