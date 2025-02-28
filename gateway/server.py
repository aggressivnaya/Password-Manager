#from flask import Flask, request, render_template, redirect, url_for, flash
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
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

@server.post("/login")
def login(request: Request, name: str, email: str):
    try:
        token = access.login(request, name, email)
        #TODO: send email
        #send.sendAuth(token)
        return {"access_token": token}
    except Exception as e:
        return e


@server.post("/signup") 
def signup(request: Request, name: str, email: str):
    try:
        token = access.token(request, name, email)
        #TODO: send email
        #send.sendAuth(token)
        return {"access_token": token}
    except Exception as e:
        return e

@server.get('/check')
def check(request: Request, code: str):
    return send.checkGeneratedCode(code)

@server.get("/passwords")
def passwords(request: Request, passwordId: int):
    try:
        access = validate.token(request)['token']
    except Exception as e:
        return e
    
    try:
        return get.getPasswords(request)
    except Exception as e:
        return e

@server.post("/passwords/add")
def passwordAdd(request: Request, password: str = None, name: str = None, shared: str = None):
    try:
        access = validate.token(request)['token']
    except Exception as e:
        return e
    
    try:
        return updating_data.addPassword(request)
    except Exception as e:
        return e
    
@server.post("/passwords/update")
def passwordUpd(request: Request, currPasswordId: int = None, newPassword: str = None, newName: str = None, shared: str = None):
    try:
        access = validate.token(request)['token']
    except Exception as e:
        return e
    
    try:
        return updating_data.updatePassword(request)
    except Exception as e:
        return e
    
@server.post("/passwords/delete")
def passwordDlt(request: Request, currPasswordId: int = None):
    try:
        access = validate.token(request)['token']
    except Exception as e:
        return e
    
    try:
        return updating_data.deletePassword(request)
    except Exception as e:
        return e

@server.get("/groups")
def groups(request: Request, groupName: str = None):
    try:
        access = validate.token(request)['token']
    except Exception as e:
        return e
    
    try:
        return get.getGroups(request)
    except Exception as e:
        return e
    
@server.get("/groups/{groupName}/passwords")
def groups(request: Request, groupName: str = None):
    try:
        access = validate.token(request)['token']
    except Exception as e:
        return e
    
    try:
        return get.getGroupPasswords(request)
    except  Exception as e:
        return e
    
@server.post("/groups/{groupName}/passwords/add")
def groups(request: Request):
    try:
        access = validate.token(request)['token']
    except Exception as e:
        return e
    
    try:
        return updating_data.addPasswordToGroup(request)
    except  Exception as e:
        return e

@server.get("/history")
def history(request: Request):
    access = validate.token(request)

    try:
        access = validate.token(request)['token']
    except Exception as e:
        return e
    
    try:
        return get.getHistory(request)
    except Exception as e:
        return e
 
@server.route('/logout')
def logout(request: Request):
    try:
        access = validate.token(request)['token']
    except Exception as e:
        return e
    
    try:
        return access.logout(request)
    except Exception as e:
        return e
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(server, host="182.20.1.2", port=5002)
    