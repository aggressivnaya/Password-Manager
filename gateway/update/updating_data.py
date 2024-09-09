import os, requests

def addPassword(username, password):
    data = {"username" : username, "curr_password" : password}

    response = requests.post(
        f"http://{os.environ.get('DATA_SVC_ADDRESS')}/changes", data=data
    )

    if response.status_code == 200:
        return response.text, None
    else:
        return None, (response.text, response.status_code)

def updatePassword(username, currPasswordID, newPassword):
    data = {"username" : username, "curr_password_id" : currPasswordID, "new_password" : newPassword}

    response = requests.post(
        f"http://{os.environ.get('DATA_SVC_ADDRESS')}/changes", data=data
    )

    if response.status_code == 200:
        return response.text, None
    else:
        return None, (response.text, response.status_code)

def deletePassword(username, password):
    data = {"username" : username, "curr_password" : password}

    response = requests.post(
        f"http://{os.environ.get('DATA_SVC_ADDRESS')}/changes", data=data
    )

    if response.status_code == 200:
        return response.text, None
    else:
        return None, (response.text, response.status_code)