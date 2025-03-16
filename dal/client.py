import os, requests
from fastapi import HTTPException, Request

DAL_SVC_ADDRESS = '182.20.1.4:5001'
token = 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InVzZXIzIiwiZW1haWwiOiIxYXNkZiIsImV4cCI6MTc0MTc4NTA1OH0.MXsZAoTnW3_LEwHX4u3IXXaASBty1075H8_KnH1u9pk'

def getPasswords():
    header = {"Authorization" : token}

    try:
        response = requests.get(
            f"http://{DAL_SVC_ADDRESS}/get",headers=header 
        )
        
        print('user passwords: ',response.json()['passwords'])
    except Exception as e:
        #raise HTTPException(status_code=400, detail="Passwords not found")
        print(e)

def getPasswordById( id):
    header = {"Authorization" : token}
    data = {"password_id" : id}

    try:
        response = requests.get(
            f"http://{DAL_SVC_ADDRESS}/get",headers=header , params=data
        )
        
        print('password by id: ',response.json()['password'])
    except Exception as e:
        #raise HTTPException(status_code=400, detail="Password not found")
        print(e)
    
    
def getHistory( passwordId=-1):
    header = {"Authorization" : token}
    if passwordId != -1:
        data = { "passwordId" : passwordId}
    else:
        data = {}

    try:
        response = requests.get(
            f"http://{DAL_SVC_ADDRESS}/history",headers=header , params=data
        )
        
        print('History: ',response.json()['history'])
    except Exception as e:
        #raise HTTPException(status_code=400, detail="History not found")
        print(e)
    

def addPassword(password):
    header = {"Authorization" : token}

    data = { "curr_password" : password}

    try:
        response = requests.post(
            f"http://{DAL_SVC_ADDRESS}/changes/add/",headers=header , data=data
        )
        print(response.json()['success'])
    except Exception as e:
        #raise HTTPException(status_code=400, detail="Password not added")
        print(e)


def updatePassword(currPasswordID, newPassword):
    header = {"Authorization" : token}

    data = {"curr_password_id" : currPasswordID, "new_password" : newPassword}

    try:
        response = requests.post(
            f"http://{DAL_SVC_ADDRESS}/changes/update/",headers=header , data=data
        )

        print(response.json()['success'])
    except Exception as e:
        #raise HTTPException(status_code=400)
        print(e)

def deletePassword(password):
    header = {"Authorization" : token}

    data = { "curr_password" : password}

    try:
        response = requests.post(
            f"http://{DAL_SVC_ADDRESS}/changes/delete/",headers=header , data=data
        )
        
        print(response.json()['success'])  
        
    except Exception as e:
        #raise HTTPException(status_code=400, detail="Password not deleted")
        print(e)
    

if __name__ == "__main__":
    getPasswords()
    #getPasswordById(1)
    #getHistory(1)
    #addPassword("testpassword")
    #updatePassword(1, "newpassword")
    #deletePassword("testpassword")
    #print("All tests passed")
