import requests, os

AUTH_SVC_ADDRESS = '182.20.1.3:5000'

username = "alice"
email = "alice.agrest@gmail.com"
token = ""

def login():
    data = {
    "name": username,
    "email": email,
    }
    try:
        response = requests.post(
            f"http://{AUTH_SVC_ADDRESS}/login/", json=data
        )
        global token
        token = response.json()['access_token']
        print(token)
    except Exception as e:
        print(e)
    
def signup():
    data = {
    "name": username,
    "email": email,
    }

    try:
        response = requests.post(
            f"http://{AUTH_SVC_ADDRESS}/signup/", json=data
        )
        global token
        token = response.json()['access_token']
        print(token)
    except Exception as e:
        print(e)

def validate(token):
    try:
        response = requests.post(
            f"http://{AUTH_SVC_ADDRESS}/validate/", headers={"Authorization": 'Bearer '+token}
        )
        print(response.json()['validated'])
    except Exception as e:
        print(e)

if __name__ == "__main__":
    signup()
    #token = login()
    #validate(token)