import requests

username = "alice"

def getPasswords(username):
    data = {"username" : username}
    response = requests.get(
        f"http://127.0.0.1:5001/get", params=data
    )

    if response.status_code == 200:
        return response.text, response.status_code
    else:
        return None, 400

def getPasswordById(id):
    data = {"password_id" : id}
    response = requests.get(
        f"http://127.0.0.1:5001/get", params=data
    )
    
    if response.status_code == 200:
        return response.text, response.status_code
    else:
        return None, 400
    
def getHistory(username, passwordId=0):
    #if passwordId == 0:
    data = {"username" : username}
    #else:
      #  data = {"username" : username, "passwordId" : passwordId}

    response = requests.get(
        f"http://127.0.0.1:5001/history", params=data
    )
    
    if response.status_code == 200:
        return response.text, response.status_code
    else:
        return None, 400
    
def addPassword(username, password):
    data = {"func": "add" ,"username" : username,"name": "aliceeee", "password" : password, "shared": "False"}

    response = requests.post(
        f"http://127.0.0.1:5001/changes", data=data
    )

    if response.status_code == 200:
        return response.text, response.status_code
    else:
        return None, 400

def updatePassword(username, currPasswordID, newPassword, name):
    data = {"func": "update" ,"username" : username, "curr_password_id" : currPasswordID, "new_password" : newPassword, "new_name": name, "shared": "False"}

    response = requests.post(
        f"http://127.0.0.1:5001/changes", data=data
    )

    if response.status_code == 200:
        return response.text, response.status_code
    else:
        return None, 400

def deletePassword(username, passwordId):
    data = {"func": "delete" ,"username" : username, "curr_password_id" : passwordId}

    response = requests.post(
        f"http://127.0.0.1:5001/changes", data=data
    )

    if response.status_code == 200:
        return response.text, response.status_code
    else:
        return None, 400
    
def signup():
    data = {"username" : username, "email" : "email"}
    response = requests.get(
        "http://127.0.0.1:5001/login", params=data
    )

    if response.status_code == 200:
        return True
    else:
        return False
    
if __name__ == "__main__":
    '''print(signup())
    print(addPassword(username, "asssa")[0])
    print(addPassword(username, "aieur")[0])
    print(getPasswords(username)[0])
    print(getPasswordById(1)[0])
    print(updatePassword(username, 2, "ddddd", "aliceeee")[0])
    print(getPasswords(username)[0])
    print(deletePassword(username, 2)[0])
    print(getPasswords(username)[0])
    print(getHistory(username)[0])
    '''