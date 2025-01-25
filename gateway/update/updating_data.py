import os, requests

def addPassword(token, password):
    header = {"Authorization" : token}
    data = { "curr_password" : password}

    response = requests.post(
        f"http://{os.environ.get('DATA_SVC_ADDRESS')}/changes",headers=header , data=data
    )

    if response.status_code == 200:
        return response.text, response.status_code
    else:
        return None, 400

def updatePassword(token, currPasswordID, newPassword):
    header = {"Authorization" : token}
    data = {"curr_password_id" : currPasswordID, "new_password" : newPassword}

    response = requests.post(
        f"http://{os.environ.get('DATA_SVC_ADDRESS')}/changes",headers=header , data=data
    )

    if response.status_code == 200:
        return response.text, response.status_code
    else:
        return None, 400

def deletePassword(token, password):
    header = {"Authorization" : token}
    data = { "curr_password" : password}

    response = requests.post(
        f"http://{os.environ.get('DATA_SVC_ADDRESS')}/changes",headers=header , data=data
    )

    if response.status_code == 200:
        return response.text, response.status_code
    else:
        return None, 400