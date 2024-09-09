import os, requests

def login(username, password):
    data = {"username" : username, "password" : password}
    response = requests.get(
        f"http://{os.environ.get('DATA_SVC_ADDRESS')}/login", params=data
    )

    if response.status_code == 200:
        return True
    else:
        return False

def signup(username, password, email):
    data = {"username" : username, "password" : password, "email" : email}
    response = requests.get(
        f"http://{os.environ.get('DATA_SVC_ADDRESS')}/login", params=data
    )

    if response.status_code == 200:
        return True
    else:
        return False