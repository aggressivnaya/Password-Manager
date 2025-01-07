import requests

username = "princessaaaa96@gmail.com"
url = "http://127.0.0.1:2343"


data = {"from_doctor" : username, "to_doctor" : "alice.agrest@gmail.com", "data":"hello guys, how r u,im under the water ,pls help me"}
response = requests.post(
    f"{url}/send_msg", data=data
)
print(response.text)