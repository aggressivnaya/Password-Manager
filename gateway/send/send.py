import requests
from fastapi import Request, HTTPException

NOTIFICATION_SVC_ADDRESS = '182.20.1.6:5003'

generatedCode = ''

def sendUpdate(request: Request, sender: str, receiver: str, data: str) -> bool:
    try:
        response = requests.post(f'http://{NOTIFICATION_SVC_ADDRESS}/sendUpdate/', params={'sender': sender, 'receiver': receiver, 'data': data})
        return True
    except Exception as e:
        raise e
    
def sendAuth(token) -> bool:
    try:
        response = requests.post(f'http://{NOTIFICATION_SVC_ADDRESS}/sendAuthentication/', headers={'Authorization': 'Bearer ' + token})
        global generatedCode
        generatedCode = response.json()['generatedCode']
        return True
    except Exception as e:
        raise e
    
def checkGeneratedCode(code: str) -> bool:
    if code == generatedCode:
        return True
    else:
        return False