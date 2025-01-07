import os, requests

url = "http://127.0.0.1:2343"

def sendEmail(email, data):
    data = {"from_doctor" : email, "to_doctor" : "alice.agrest@gmail.com", "data" : data}
    response = requests.post(
        f"{url}/send_msg", data=data
    )

    return response.status_code