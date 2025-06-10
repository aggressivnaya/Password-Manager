import requests
from fastapi import Request, HTTPException

NOTIFICATION_SVC_ADDRESS = '182.20.1.6:5003'

generatedCode = ''

def sendUpdate(request: Request ,token , receiver: str, subj: str, data: str) -> bool:
    try:
        response = requests.post(f'http://{NOTIFICATION_SVC_ADDRESS}/sendUpdate/', headers={'Authorization': 'Bearer ' + token}, params={ 'receiver': receiver,'subj': subj, 'data': data})
        if response.json()['status'] == 200:
            print("Update sent successfully")
            return True
        else: 
            print("Failed to send update")
            return False
    except Exception as e:
        return False
    
def sendAuth(token) -> bool:
    try:
        response = requests.post(f'http://{NOTIFICATION_SVC_ADDRESS}/sendAuthentication/', headers={'Authorization': 'Bearer ' + token})
        global generatedCode
        generatedCode = response.json()['generatedCode']
        print(f"Generated code: {generatedCode}")
        return True
    except Exception as e:
        return False
    
def checkGeneratedCode(code: str) -> bool:
    if code == str(generatedCode):
        return True
    else:
        return False