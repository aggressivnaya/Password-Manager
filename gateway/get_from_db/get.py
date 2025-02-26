import os, requests
from fastapi import HTTPException, Request

DATA_SVC_ADDRESS = '182.20.1.4:5001'

def getPasswords(request: Request):
    header = {"Authorization" : request.header.get('Authorization')}

    try:
        response = requests.get(
            f"http://{DATA_SVC_ADDRESS}/get",headers=header 
        )
        return {'passwords': response.json()['passwords']}
    except:
        raise HTTPException(status_code=400, detail="Passwords not found")

def getPasswordById(request: Request, id):
    header = {"Authorization" : request.header.get('Authorization')}
    data = {"password_id" : id}

    try:
        response = requests.get(
            f"http://{DATA_SVC_ADDRESS}/get",headers=header , params=data
        )
        return {'password': response.json()['password']}
    except:
        raise HTTPException(status_code=400, detail="Password not found")
    
    
def getHistory(request: Request, passwordId=-1):
    header = {"Authorization" : request.header.get('Authorization')}
    if passwordId != -1:
        data = { "passwordId" : passwordId}
    else:
        data = {}

    try:
        response = requests.get(
            f"http://{DATA_SVC_ADDRESS}/history",headers=header , params=data
        )
        return {'history': response.json()['history']}
    except:
        raise HTTPException(status_code=400, detail="History not found")
    