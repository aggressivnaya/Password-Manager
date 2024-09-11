import os, requests

def addPassword(username, password):
    data = {"username" : username, "curr_password" : password}

    response = requests.post(
        f"http://{os.environ.get('DATA_SVC_ADDRESS')}/changes", data=data
    )

    if response.status_code == 200:
        return response.text, response.status_code
    else:
        return None, 400

def updatePassword(username, currPasswordID, newPassword):
    data = {"username" : username, "curr_password_id" : currPasswordID, "new_password" : newPassword}

    response = requests.post(
        f"http://{os.environ.get('DATA_SVC_ADDRESS')}/changes", data=data
    )

    if response.status_code == 200:
        return response.text, response.status_code
    else:
        return None, 400

def deletePassword(username, password):
    data = {"username" : username, "curr_password" : password}

    response = requests.post(
        f"http://{os.environ.get('DATA_SVC_ADDRESS')}/changes", data=data
    )

    if response.status_code == 200:
        return response.text, response.status_code
    else:
        return None, 400