import requests, os

def login():
    username = "alice"
    email = "alice@gmail.com"

    basicAuth = (username, "fff")

    response = requests.post(
        "http://127.0.0.1:5000/login", auth=basicAuth
    )

    if response.status_code == 200:
        print("response: " + response.text)
        return response.text
    else:
        print("error with login")
    
def signup():
    username = "alice"
    email = "alice@gmail.com"

    basicAuth = (username, email)

    response = requests.post(
        "http://127.0.0.1:5000/signup", auth=basicAuth
    )

    if response.status_code == 200:
        print("response: " + response.text)
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