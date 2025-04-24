import requests

username = "princessaaaa96@gmail.com"
url = "http://182.20.1.6:5003"


data = {"sender": username, "receiver": "alice.agrest@gmail.com", "data": "Hello Alice!"}
response = requests.post(
    f"{url}/sendUpdate/", params=data
)
print(response.text)