import os, requests

def getPasswords(username):
    data = {"username" : username}
    response = requests.get(
        f"http://{os.environ.get('DATA_SVC_ADDRESS')}/get", params=data
    )

    if response.status_code == 200:
        return response.text, None
    else:
        return None, (response.text, response.status_code)

def getPasswordById(id):
    data = {"password_id" : id}
    response = requests.get(
        f"http://{os.environ.get('DATA_SVC_ADDRESS')}/get", params=data
    )
    
    if response.status_code == 200:
        return response.text, None
    else:
        return None, (response.text, response.status_code)