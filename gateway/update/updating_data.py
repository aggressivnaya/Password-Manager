import os, requests
from fastapi import HTTPException, Request

DATA_SVC_ADDRESS = '182.20.1.4:5001'

def addPassword(request, password):
    header = {"Authorization" : request.header.get('Authorization')}

    data = { "curr_password" : password}

    try:
        response = requests.post(
            f"http://{DATA_SVC_ADDRESS}/changes/add/",headers=header , data=data
        )
        return True
    except:
        #raise HTTPException(status_code=400, detail="Password not added")
        return False


def updatePassword(request, currPasswordID, newPassword):
    header = {"Authorization" : request.header.get('Authorization')}

    data = {"curr_password_id" : currPasswordID, "new_password" : newPassword}

    try:
        response = requests.post(
            f"http://{DATA_SVC_ADDRESS}/changes/update/",headers=header , data=data
        )

        if response.json()['success']:
            return True
        return False
    except:
        #raise HTTPException(status_code=400)
        return False

def deletePassword(request, password):
    header = {"Authorization" : request.header.get('Authorization')}

    data = { "curr_password" : password}

    try:
        response = requests.post(
            f"http://{DATA_SVC_ADDRESS}/changes/delete/",headers=header , data=data
        )
        
        if response.json()['success']:
            return True
        return False
    except:
        #raise HTTPException(status_code=400, detail="Password not deleted")
        return False

#TODO: implement this
def addPasswordToGroup(request, group):
    header = {"Authorization" : request.header.get('Authorization')}

    data = { "curr_group" : group}

    try:
        response = requests.post(
            f"http://{DATA_SVC_ADDRESS}/",headers=header , data=data
        )

        if response.json()['success']:
            return True
        return False
    except:
        raise HTTPException(status_code=400, detail="Group not added")
