import os, requests

def login(username):
    data = {"username" : username}
    response = requests.get(
        "http://127.0.0.1:5001/login", params=data
    )

    if response.status_code == 200:
        return True
    else:
        return False

def signup(username,  email):
    data = {"username" : username, "email" : email}
    response = requests.get(
        "http://127.0.0.1:5001/login", params=data
    )

    if response.status_code == 200:
        return True
    else:
        return False