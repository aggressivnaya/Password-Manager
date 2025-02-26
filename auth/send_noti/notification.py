import os, requests

url = "http://127.0.0.1:2343"

def sendEmail(email, data):
    data = {"sender" : email, "to" : "alice.agrest@gmail.com",'subject': 'Authentication Code', "body" : data}
    response = requests.post(
        f"{url}/send_msg", data=data
    )

    return response.status_code