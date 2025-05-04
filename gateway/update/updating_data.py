import os, requests
from fastapi import HTTPException, Request

DATA_SVC_ADDRESS = '182.20.1.4:5001'

def addPassword(token, password, name, shared):
    header={"Authorization": f"Bearer {token}"}

    params={"password": password, "name": name, "shared": shared}
    
    try:
        print('adding password')
        response = requests.post(
            f"http://{DATA_SVC_ADDRESS}/PrivatePasswords/add/",headers=header , params=params
        )
        print(response.json())
        return response.json()
    except:
        #raise HTTPException(status_code=400, detail="Password not added")
        return False


def updatePassword(token, currPasswordID, newPassword, newName, shared):
    header={"Authorization": f"Bearer {token}"}

    data = {"currPasswordId" : currPasswordID, "newPassword" : newPassword, "newName": newName, "shared": shared}

    try:
        response = requests.post(
            f"http://{DATA_SVC_ADDRESS}/PrivatePasswords/update/",headers=header , params=data
        )

        return response.json()
    except:
        #raise HTTPException(status_code=400)
        return False

def deletePassword(token, passwordId):
    header={"Authorization": f"Bearer {token}"}

    data = { "currPasswordId" : passwordId}

    try:
        response = requests.delete(
            f"http://{DATA_SVC_ADDRESS}/PrivatePasswords/delete/",headers=header , params=data
        )
        
        return response.json()
    except:
        #raise HTTPException(status_code=400, detail="Password not deleted")
        return False

def addPasswordGroup(token, group, password, shared, name):
    header={"Authorization": f"Bearer {token}"}

    data = { "groupName" : group, "password": password, "name": name, "shared": shared}

    try:
        response = requests.post(
            f"http://{DATA_SVC_ADDRESS}/group/addPassword",headers=header , params=data
        )

        return response.json()
    except:
        raise HTTPException(status_code=400, detail="Group not added")
    
def updatePasswordGroup(token, group, currPasswordID, newPassword, newName, shared):
    header={"Authorization": f"Bearer {token}"}

    data = {"groupName" : group, "passwordId" : currPasswordID, "newPassword" : newPassword, "newName": newName, "shared": shared}

    try:
        response = requests.post(
            f"http://{DATA_SVC_ADDRESS}/group/updPassword",headers=header , params=data
        )

        return response.json()
    except:
        raise HTTPException(status_code=400)
    
def deletePasswordGroup(token, group, password):
    header={"Authorization": f"Bearer {token}"}

    data = { "groupName" : group, "passwordId" : password}

    try:
        response = requests.post(
            f"http://{DATA_SVC_ADDRESS}/group/removePassword",headers=header , params=data
        )

        return response.json()
    except:
        raise HTTPException(status_code=400, detail="Group not deleted")
    
def createGroup(token, name, description):
    header={"Authorization": f"Bearer {token}"}

    data = {"name": name, "description": description}

    try:
        response = requests.post(
            f"http://{DATA_SVC_ADDRESS}/group/create_group",headers=header , params=data
        )

        return response.json()
    except:
        raise HTTPException(status_code=400, detail="Group not created")

def deleteGroup(token, group):
    header={"Authorization": f"Bearer {token}"}

    data = { "groupName" : group}

    try:
        response = requests.delete(
            f"http://{DATA_SVC_ADDRESS}/group/remove_group",headers=header , params=data
        )

        return response.json()
    except:
        raise HTTPException(status_code=400, detail="Group not deleted")
    
def addUserToGroup(token, group, user):
    header={"Authorization": f"Bearer {token}"}

    data = { "groupName" : group, "username": user}

    try:
        response = requests.post(
            f"http://{DATA_SVC_ADDRESS}/group/accept_user",headers=header , params=data
        )

        return response.json()
    except:
        raise HTTPException(status_code=400, detail="User not added")
    
def removeUserFromGroup(token, group, user):
    header={"Authorization": f"Bearer {token}"}

    data = { "groupName" : group, "username": user}

    try:
        response = requests.post(
            f"http://{DATA_SVC_ADDRESS}/group/remove_user",headers=header , params=data
        )

        return response.json()
    except:
        raise HTTPException(status_code=400, detail="User not removed")
    
def leaveGroup(token, group):
    header={"Authorization": f"Bearer {token}"}

    data = { "groupName" : group}

    try:
        response = requests.delete(
            f"http://{DATA_SVC_ADDRESS}/group/leave_group",headers=header , params=data
        )

        return response.json()
    except:
        raise HTTPException(status_code=400, detail="Group not left")
'''   
def enterGroup(token, group):
    header={"Authorization": f"Bearer {token}"}

    data = { "groupLink" : group}

    try:
        response = requests.get(
            f"http://{DATA_SVC_ADDRESS}/group/enter_group",headers=header , params=data
        )

        return response.json()
    except:
        raise HTTPException(status_code=400, detail="Group not entered")'''

def insertRequest(token, group, requestCommand):
    header={"Authorization": f"Bearer {token}"}

    data = { "groupName" : group, "requestCommand": requestCommand}

    try:
        response = requests.post(
            f"http://{DATA_SVC_ADDRESS}/group/insert_request",headers=header , params=data
        )

        return response.json()
    except:
        raise HTTPException(status_code=400, detail="Request not sent")
    
def acceptRequest(token, group, requestId):
    header={"Authorization": f"Bearer {token}"}

    data = { "groupName" : group, "requestId": requestId}

    try:
        response = requests.post(
            f"http://{DATA_SVC_ADDRESS}/group/approve_request",headers=header , params=data
        )

        return response.json()
    except:
        raise HTTPException(status_code=400, detail="Request not accepted")
    
def denyRequest(token, group, requestId):
    header={"Authorization": f"Bearer {token}"}

    data = { "groupName" : group, "requestId": requestId}

    try:
        response = requests.post(
            f"http://{DATA_SVC_ADDRESS}/group/deny_request",headers=header , params=data
        )

        return response.json()
    except:
        raise HTTPException(status_code=400, detail="Request not rejected")

#if __name__ == "__main__":
   # addPassword( "password", "name", False)