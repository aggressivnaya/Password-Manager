import os, requests
from fastapi import HTTPException, Request

DATA_SVC_ADDRESS = '182.20.1.4:5001'

def getUser(token):
    header={"Authorization": f"Bearer {token}"}
    
    try:
        print('getting user')
        response = requests.get(
            f"http://{DATA_SVC_ADDRESS}/user",headers=header 
        )
        return {'user': response.json()['user']}
    except:
        raise HTTPException(status_code=400, detail="User not found")

def getPasswords(token):
    header={"Authorization": f"Bearer {token}"}

    try:
        print('getting passwords')
        response = requests.get(
            f"http://{DATA_SVC_ADDRESS}/getPasswords",headers=header 
        )
        return {'passwords': response.json()['passwords']}
    except:
        #raise HTTPException(status_code=400, detail="Passwords not found")
        return {'passwords': []}

def getPasswordById(token, id):
    header={"Authorization": f"Bearer {token}"}
    data = {"passwordId" : id}

    try:
        print('getting password')
        response = requests.get(
            f"http://{DATA_SVC_ADDRESS}/getPassword",headers=header , params=data
        )
        return {'password': response.json()['password']}
    except:
        raise HTTPException(status_code=400, detail="Password not found")
    
    
def getHistory(token):
    header={"Authorization": f"Bearer {token}"}
    try:
        response = requests.get(
            f"http://{DATA_SVC_ADDRESS}/history",headers=header 
        )
        print('getting history')
        print(response.json()['history'])
        return {'history': response.json()['history']}
    except:
        return {'history': []}
    
def getNotifications(token):
    header={"Authorization": f"Bearer {token}"}
    try:
        response = requests.get(
            f"http://{DATA_SVC_ADDRESS}/notifications",headers=header 
        )
        print('getting notifications')
        print(response.json()['notifications'])
        return {'notifications': response.json()['notifications']}
    except:
        return {'notifications': []}
    
def getGroups(token):
    header={"Authorization": f"Bearer {token}"}

    try:
        response = requests.get(
            f"http://{DATA_SVC_ADDRESS}/groups",headers=header 
        )
        return {'groups': response.json()['groups']}
    except:
        return {'groups': []}

def getRequestedGroup(token, group):
    header={"Authorization": f"Bearer {token}"}
    data = { "groupName" : group}

    try:
        response = requests.get(
            f"http://{DATA_SVC_ADDRESS}/group",headers=header , params=data
        )
        return {'group': response.json()['groupinfo']}
    except:
        raise HTTPException(status_code=400, detail="Group not found")
    
def getAdminGroup(token, group):
    header={"Authorization": f"Bearer {token}"}
    data = { "groupName" : group}

    try:
        response = requests.get(
            f"http://{DATA_SVC_ADDRESS}/group/admin_user",headers=header , params=data
        )
        return {'admin': response.json()['admin']}
    except:
        raise HTTPException(status_code=400, detail="Group not found")
    
def getGroupRequests(token, group):
    header={"Authorization": f"Bearer {token}"}
    data = { "groupName" : group}

    try:
        response = requests.get(
            f"http://{DATA_SVC_ADDRESS}/group/requests",headers=header , params=data
        )
        print(response.json()["requests"])
        return {'requests': response.json()['requests']}
    except:
        return {'requests': []}