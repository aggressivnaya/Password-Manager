import os, requests

def getPasswords(token):
    header = {"Authorization" : token}
    response = requests.get(
        f"http://{os.environ.get('DATA_SVC_ADDRESS')}/get",headers=header 
    )

    if response.status_code == 200:
        return response.text, response.status_code
    else:
        return None, 400

def getPasswordById(token, id):
    header = {"Authorization" : token}
    data = {"password_id" : id}
    response = requests.get(
        f"http://{os.environ.get('DATA_SVC_ADDRESS')}/get",headers=header , params=data
    )
    
    if response.status_code == 200:
        return response.text, response.status_code
    else:
        return None, 400
    
def getHistory(token, passwordId=-1):
    header = {"Authorization" : token}
    if passwordId != -1:
        data = { "passwordId" : passwordId}
    else:
        data = {}

    response = requests.get(
        f"http://{os.environ.get('DATA_SVC_ADDRESS')}/history",headers=header , params=data
    )
    
    if response.status_code == 200:
        return response.text, response.status_code
    else:
        return None, 400