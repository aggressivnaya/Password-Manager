import datetime, os, jwt, random
from pydantic import BaseModel
from fastapi import FastAPI, Request, HTTPException
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
import os
import sys
sys.path.append(os.path.abspath('..'))
#from dal.classes.usersDb import User
from common.classes import User
from common.base import session_factory
from send_noti import notification

server = FastAPI()
db = session_factory()
server.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

class BodyUser(BaseModel):
    name: str
    email: str

@server.post("/login/")
def login(user: BodyUser):
    findingUser = (db.query(User).filter(User.username == user.name and User.email == user.email).all())[0]
    if findingUser != None:
        return {"access_token": createToken(user.name ,user.email)}
    else:
        raise HTTPException(status_code=401, detail="invalid credentials")
    
@server.post('/signup/')
def signup(user: User):
    findingUser = (db.query(User).filter(User.username == user.name and User.email == user.email).all())[0]
    if findingUser == None:
        db.add(User(user.name, user.email))
        return {"access_token": createToken(user.name, user.email)}
    else:
        raise HTTPException(status_code=401, detail="invalid credentials")

def createToken(username, email) -> str:
    return jwt.encode(
        {
            "username": username,
            "email": email,
            "exp": datetime.datetime.now() + datetime.timedelta(days=1),
        },
        "SARCASM",
        algorithm="HS256"
    )

oauth2Schema = OAuth2PasswordBearer(tokenUrl="/login/")

@server.post("/validate/")
def validate(request: Request):
    authHeader = request.headers.get("Authorization")
    if not authHeader:
        raise HTTPException(status_code=401, detail="not authorized")

    parts = authHeader.split(" ")
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(status_code=401, detail="not authorized")
    
    encoded_jwt = parts[1]
    if not encoded_jwt:
        raise HTTPException(status_code=401, detail="not authorized")

    try:
        decoded = jwt.decode(
            encoded_jwt, "SARCASM", algorithms=["HS256"]
        )
        isExpired = datetime.datetime.fromtimestamp(decoded["exp"]) < datetime.datetime.utcnow()

        findingUser = (db.query(User).filter(User.username == decoded["username"] and User.email == decoded['email']).all())[0]
        if not findingUser and not isExpired:
            raise HTTPException(status_code=401, detail="not authorized")
    except:
        raise HTTPException(status_code=401, detail="not authorized")

    return {"validated": True}
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(server, host="182.20.1.3", port=5000)
    
