import requests

username = "princessaaaa96@gmail.com"
url = "http://182.20.1.6:5003"


data = {"sender": username, "receiver": "alice.agrest@gmail.com", "data": "Hello Alice!"}
response = requests.post(
    f"{url}/sendUpdate/",headers={"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InVzZXIxIiwiZW1haWwiOiJ1c2VyMUBleGFtcGxlLmNvbSIsImV4cCI6MTc0NTU5OTA1OX0.A0M-wavwku_GfKFzrOjzQv4MWbCibMZdumkimZczoZE"}
    , params=data
)
print(response.text)