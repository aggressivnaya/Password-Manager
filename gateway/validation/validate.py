import os, requests

AUTH_SVC_ADDRESS = '182.20.1.3:5000'

#this checking if the authorization in the header exist 
#also if the token is right
def token(request):
    try:
        response = requests.post(
            f"http://{AUTH_SVC_ADDRESS}/validate/",
            headers=request.headers,
        )
        return response.json()['validated']
    except Exception as e:
        raise e