import os, requests

AUTH_SVC_ADDRESS = '182.20.1.3:5000'
DATA_SVC_ADDRESS = '182.20.1.4:5001'

#this is connecting to auth service and getting the token from the server if the client exist
def login(request, name, email):
    response = requests.post(
        f"http://{AUTH_SVC_ADDRESS}/login", params={'name': name, 'email': email}
    )

    if response.json()['token']:
        return response.json()['token']
    
    return None
    
    
def signup(request, name ,email):
    response = requests.post(
        f"http://{AUTH_SVC_ADDRESS}/signup", params={'name': name, 'email': email}
    )

    if response.json()['token']:
        return response.json()['token']

    return None


def check(request, code):
    response = requests.get(
        f"http://{AUTH_SVC_ADDRESS}/check", params={'code': code}
    )

    if response.json()['success']:
        return True

    return False

def logout(request):
    headers = {"Authorization" : request.headers.get('Authorization')}
    try:
        response = requests.post(
            f"http://{DATA_SVC_ADDRESS}/logout/", headers=headers)
        
        if response.json()['success']:
            return True
    except Exception as e:
        print(e)
        return False
    