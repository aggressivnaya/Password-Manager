import requests, os

username = "alice"
email = "alice.agrest@gmail.com"

def login():
    data = {
    "name": username,
    "email": email,
    }

    response = requests.post(
        "http://127.0.0.1:5000/login/", json=data
    )

    if response.status_code == 200:
        print("response: " + response.json['token'])
        #return response.text
    else:
        print("error with login")
    
def signup():
    data = {
    "name": username,
    "email": email,
    }

    response = requests.post(
        "http://127.0.0.1:5000/signup/", json=data
    )

    if response.status_code == 200:
        response.json['token']
    else:
        print("error with signup")

def validate(token):
    response = requests.post(
        "http://127.0.0.1:5000/validate", headers={"Authorization": token}
    )

    if response.status_code == 200:
        print("response: " + response.text)
    else:
        print(response.text)

if __name__ == "__main__":
    signup()
    #token = login()
    #validate(token)