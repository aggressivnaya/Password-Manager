#from flask import Flask, request, render_template, redirect, url_for, flash
from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Annotated
from validation import validate
from auth_login import access
from get_from_db import get
from update import updating_data
from send import send

server = FastAPI()
server.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

oauth2Schema = OAuth2PasswordBearer(tokenUrl="placeholder")

class BodyUser(BaseModel):
    username: str
    email: str

class Token(BaseModel):
    access_token: str
    token_type: str

@server.post("/login")
def login(request: Request, user: BodyUser):
    try:

        token = access.login(request, user.username, user.email)
        print('token: ',token)
        if token == None:
            return HTTPException(status_code=401, detail="invalid credentials")
        #TODO: send email
        if send.sendAuth(token):
            return {"access_token":token, "token_type":"bearer"}
    except Exception as e:
        return e

@server.post("/signup") 
def signup(request: Request, user: BodyUser):
    try:
        print('user: ', user.username, user.email)
        token = access.signup(request, user.username, user.email)
        print('token: ',token)
        if token == None:
            return HTTPException(status_code=401, detail="invalid credentials")
        #TODO: send email
        if send.sendAuth(token):
            return {"access_token":token, "token_type":"bearer"}
    except Exception as e:
        return e

@server.get('/check')
def check(request: Request, token: Annotated[str, Depends(oauth2Schema)], code: str):
    '''This func is checking the authentication code that was sent to the user email'''
    try:
        access = validate.token(token)
    except Exception as e:
        return e
    print("here")
    return {"success": (200 if send.checkGeneratedCode(code) else 403)}

@server.get("/user")
def user(request: Request, token: Annotated[str, Depends(oauth2Schema)]):
    try:
        access = validate.token(token)
    except Exception as e:
        return e
    
    try:
        return get.getUser(token)
    except Exception as e:
        return e

@server.get("/passwords")
def passwords(request: Request, token: Annotated[str, Depends(oauth2Schema)]):
    try:
        access = validate.token(token)
    except Exception as e:
        return e
    
    try:
        return get.getPasswords(token)
    except Exception as e:
        return e

@server.post("/passwords/add")
def passwordAdd(request: Request, token: Annotated[str, Depends(oauth2Schema)], password: str = None, name: str = None, shared: str = None):
    try:
        validate.token(token)
    except Exception as e:
        return e
    
    try:
        print('token', token)
        return updating_data.addPassword(token, password, name, shared)
    except Exception as e:
        return e
    
@server.post("/passwords/update")
def passwordUpd(request: Request, token: Annotated[str, Depends(oauth2Schema)], currPasswordId: int = None, newPassword: str = None, newName: str = None, shared: str = None):
    try:
        access = validate.token(token)
    except Exception as e:
        return e
    
    try:
        return updating_data.updatePassword(token, currPasswordId, newPassword, newName, shared)
    except Exception as e:
        return e
    
@server.delete("/passwords/delete")
def passwordDlt(request: Request, token: Annotated[str, Depends(oauth2Schema)], currPasswordId: int = None):
    try:
        access = validate.token(token)
    except Exception as e:
        return e
    
    try:
        return updating_data.deletePassword(token, currPasswordId)
    except Exception as e:
        return e

@server.get("/groups")
def groups(request: Request, token: Annotated[str, Depends(oauth2Schema)]):
    try:
        access = validate.token(token)
    except Exception as e:
        return e
    
    try:
        return get.getGroups(token)
    except Exception as e:
        return e

@server.get("/groups/{groupName}")
def group(request: Request, token: Annotated[str, Depends(oauth2Schema)], groupName: str = None):
    try:
        access = validate.token(token)
    except Exception as e:
        return e
    
    try:
        return get.getRequestedGroup(token, groupName)
    except Exception as e:
        return e
    
@server.post("/groups/{groupName}/passwords/add")
def addPassGroup(request: Request, token: Annotated[str, Depends(oauth2Schema)], groupName: str = None, password: str = None, name: str = None, shared: str = None):
    try:
        access = validate.token(token)
    except Exception as e:
        return e
    
    try:
        return updating_data.addPasswordToGroup(token, groupName, password,shared, name)
    except  Exception as e:
        return e
    
@server.delete("/groups/{groupName}/passwords/delete")
def delPassGroup(request: Request, token: Annotated[str, Depends(oauth2Schema)], groupName: str = None, passwordId: int = None):
    try:
        access = validate.token(token)
    except Exception as e:
        return e
    
    try:
        return updating_data.deletePasswordFromGroup(token, groupName, passwordId)
    except  Exception as e:
        return e
    
@server.post("/groups/{groupName}/passwords/update")
def updPassGroup(request: Request, token: Annotated[str, Depends(oauth2Schema)], groupName: str = None, passwordId: int = None, newPassword: str = None, newName: str = None, shared: str = None):
    try:
        access = validate.token(token)
    except Exception as e:
        return e
    
    try:
        return updating_data.updatePasswordInGroup(token, groupName, passwordId, newPassword, newName, shared)
    except  Exception as e:
        return e
    
@server.post("/groups/{groupName}/createGroup")
def createGroup(request: Request, token: Annotated[str, Depends(oauth2Schema)], groupName: str = None, description: str = None):
    try:
        access = validate.token(token)
    except Exception as e:
        return e
    
    try:
        return updating_data.createGroup(token, groupName, description)
    except  Exception as e:
        return e
    
@server.post('/groups/{groupName}/enterGroup')
def enterGroup(request: Request, token: Annotated[str, Depends(oauth2Schema)], groupName: str = None):
    try:
        access = validate.token(token)
    except Exception as e:
        return e
    
    try:
        return updating_data.insertRequest(token, groupName, "ent")
    except  Exception as e:
        return e

@server.post("/groups/{groupName}/acceptUser")
def acceptUser(request: Request, token: Annotated[str, Depends(oauth2Schema)], groupName: str = None, username: str = None):
    try:
        access = validate.token(token)
    except Exception as e:
        return e
    
    try:
        return updating_data.addUserToGroup(token, groupName, username)
    except  Exception as e:
        return e
    
@server.delete("/groups/{groupName}/removeUser")
def removeUser(request: Request, token: Annotated[str, Depends(oauth2Schema)], groupName: str = None, user: str = None):
    try:
        access = validate.token(token)
    except Exception as e:
        return e
    
    try:
        return updating_data.removeUserFromGroup(token, groupName, user)
    except  Exception as e:
        return e
    
@server.post("/groups/{groupName}/approveRequest")
def approveRequest(request: Request, token: Annotated[str, Depends(oauth2Schema)], groupName: str = None, requestId: int = None):
    try:
        access = validate.token(token)
    except Exception as e:
        return e
    
    try:
        return updating_data.acceptRequest(token, groupName, requestId)
    except  Exception as e:
        return e

@server.post("/groups/{groupName}/insertRequest")
def insertRequest(request: Request, token: Annotated[str, Depends(oauth2Schema)], groupName: str = None, command: str = None):
    try:
        access = validate.token(token)
    except Exception as e:
        return e
    
    try:
        return updating_data.insertRequest(token, groupName, command)
    except  Exception as e:
        return e 

@server.delete("/groups/{groupName}/declineRequest")
def declineRequest(request: Request, token: Annotated[str, Depends(oauth2Schema)], groupName: str = None, requestId: str = None):
    try:
        access = validate.token(token)
    except Exception as e:
        return e
    
    try:
        return updating_data.denyRequest(token, groupName, requestId)
    except  Exception as e:
        return e
    
@server.get("/groups/{groupName}/requests")
def requests(request: Request, token: Annotated[str, Depends(oauth2Schema)], groupName: str = None):
    try:
        access = validate.token(token)
    except Exception as e:
        return e
    
    try:
        return get.getGroupRequests(token, groupName)
    except Exception as e:
        return e
    
@server.delete("/groups/{groupName}/leaveGroup")
def leaveGroup(request: Request, token: Annotated[str, Depends(oauth2Schema)], groupName: str = None):
    try:
        access = validate.token(token)
    except Exception as e:
        return e
    
    try:
        return updating_data.leaveGroup(token, groupName)
    except  Exception as e:
        return e
    
@server.delete("/groups/{groupName}/removeGroup")
def removeGroup(request: Request, token: Annotated[str, Depends(oauth2Schema)], groupName: str = None):
    try:
        access = validate.token(token)
    except Exception as e:
        return e
    
    try:
        return updating_data.deleteGroup(token, groupName)
    except  Exception as e:
        return e

@server.get("/history")
def history(request: Request, token: Annotated[str, Depends(oauth2Schema)]):
    try:
        access = validate.token(token)
    except Exception as e:
        return e
    
    try:
        return get.getHistory(token)
    except Exception as e:
        return e
    
@server.get("/notifications")
def history(request: Request, token: Annotated[str, Depends(oauth2Schema)]):
    try:
        access = validate.token(token)
    except Exception as e:
        return e
    
    try:
        return get.getNotifications(token)
    except Exception as e:
        return e
 
@server.delete('/logout')
def logout(request: Request, token: Annotated[str, Depends(oauth2Schema)]):
    try:
        access = validate.token(token)
    except Exception as e:
        return e
    
    try:
        return access.logout(token)
    except Exception as e:
        return e
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(server, host="182.20.1.2", port=5002)
    #uvicorn.run(server, host="127.0.0.1", port=5002)
    