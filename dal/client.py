import os, requests
from fastapi import HTTPException, Request

DAL_SVC_ADDRESS = '182.20.1.4:5001'
token = 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InVzZXIzIiwiZW1haWwiOiIxYXNkZiIsImV4cCI6MTc0MTYzNzg0MH0.TPe9UBgXnYlf6axw_BDzZmD0Ks9leqfyiyK8ozjDt6s'

def getPasswords(request: Request):
    header = {"Authorization" : token}

    try:
        response = requests.get(
            f"http://{DAL_SVC_ADDRESS}/get",headers=header 
        )
        return {'passwords': response.json()['passwords']}
    except:
        raise HTTPException(status_code=400, detail="Passwords not found")

def getPasswordById(request: Request, id):
    header = {"Authorization" : token}
    data = {"password_id" : id}

    try:
        response = requests.get(
            f"http://{DAL_SVC_ADDRESS}/get",headers=header , params=data
        )
        return {'password': response.json()['password']}
    except:
        raise HTTPException(status_code=400, detail="Password not found")
    
    
def getHistory(request: Request, passwordId=-1):
    header = {"Authorization" : token}
    if passwordId != -1:
        data = { "passwordId" : passwordId}
    else:
        data = {}

    try:
        response = requests.get(
            f"http://{DAL_SVC_ADDRESS}/history",headers=header , params=data
        )
        return {'history': response.json()['history']}
    except:
        raise HTTPException(status_code=400, detail="History not found")
    

def addPassword(request, password):
    header = {"Authorization" : token}

    data = { "curr_password" : password}

    try:
        response = requests.post(
            f"http://{DAL_SVC_ADDRESS}/changes/add/",headers=header , data=data
        )
        return True
    except:
        #raise HTTPException(status_code=400, detail="Password not added")
        return False


def updatePassword(request, currPasswordID, newPassword):
    header = {"Authorization" : token}

    data = {"curr_password_id" : currPasswordID, "new_password" : newPassword}

    try:
        response = requests.post(
            f"http://{DAL_SVC_ADDRESS}/changes/update/",headers=header , data=data
        )

        if response.json()['success']:
            return True
        return False
    except:
        #raise HTTPException(status_code=400)
        return False

def deletePassword(request, password):
    header = {"Authorization" : token}

    data = { "curr_password" : password}

    try:
        response = requests.post(
            f"http://{DAL_SVC_ADDRESS}/changes/delete/",headers=header , data=data
        )
        
        if response.json()['success']:
            return True
        return False
    except:
        #raise HTTPException(status_code=400, detail="Password not deleted")
        return False
    

if __name__ == "__main__":
    getPasswords(Request)
    getPasswordById(Request, 1)
    getHistory(Request, 1)
    addPassword(Request, "testpassword")
    updatePassword(Request, 1, "newpassword")
    deletePassword(Request, "testpassword")
    print("All tests passed")
