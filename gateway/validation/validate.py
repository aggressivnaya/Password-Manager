import os, requests

AUTH_SVC_ADDRESS = '182.20.1.3:5000'

#this checking if the authorization in the header exist 
#also if the token is right
def token(token):
    try:
        response = requests.post(
            f"http://{AUTH_SVC_ADDRESS}/validate/",
            headers={"Authorization": f"Bearer {token}"},
        )
        return response.json()['validated']
    except Exception as e:
        raise e