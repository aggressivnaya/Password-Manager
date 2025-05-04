import requests

DAL_SVC_ADDRESS = '182.20.1.4:5001'
AUTH_SVC_ADDRESS = '182.20.1.3:5000'

token = ""
def login():
    data = {
    "username": "user1",
    "email": "user1@example.com",
    }
    try:
        response = requests.post(
            f"http://{AUTH_SVC_ADDRESS}/login/", json=data
        )
        global token
        token = response.json()['access_token']
        print(token)
    except Exception as e:
        print(e)

def test_add_password():
    response = requests.post(
        "http://"+ DAL_SVC_ADDRESS + "/changes/add/",
        headers={"Authorization": f"Bearer {token}"},
        params={"password": "testpassword", "name": "testname", "shared": "False"}
    )
    response = requests.post(
        "http://"+ DAL_SVC_ADDRESS + "/changes/add/",
        headers={"Authorization": f"Bearer {token}"},
        params={"password": "ert", "name": "123", "shared": "False"}
    )
    response = requests.post(
        "http://"+ DAL_SVC_ADDRESS + "/changes/add/",
        headers={"Authorization": f"Bearer {token}"},
        params={"password": "errrrrt", "name": "456", "shared": "False"}
    )
    response = requests.post(
        "http://"+ DAL_SVC_ADDRESS + "/changes/add/",
        headers={"Authorization": f"Bearer {token}"},
        params={"password": "fgh", "name": "678", "shared": "False"}
    )
    print(response.json()["success"])

def test_update_password():
    response = requests.post(
        "http://"+ DAL_SVC_ADDRESS + "/changes/update/",
        headers={"Authorization": f"Bearer {token}"},
        params={"currPasswordId": 6, "newPassword": "newpassword", "newName": "newname", "shared": "False"}
    )
    #assert response.status_code == 200
    #assert response.json() == {"success", 200}
    print(response.json())

def test_delete_password():
    response = requests.delete(
        "http://"+ DAL_SVC_ADDRESS + "/changes/delete/",
        headers={"Authorization": f"Bearer {token}"},
        params={"currPasswordId": 1}
    )
    print(response.json())

def test_get_required_password():
    response = requests.get("http://"+ DAL_SVC_ADDRESS + "/getPassword",headers={"Authorization": f"Bearer {token}"}, params={"passwordId": 3})
    print(response.json()['password'])

def test_get_user_passwords():
    response = requests.get("http://"+ DAL_SVC_ADDRESS + "/getPasswords", headers={"Authorization": f"Bearer {token}"})
    print(response.json()['passwords'])

def test_history():
    response = requests.get("http://"+ DAL_SVC_ADDRESS + "/history", headers={"Authorization": f"Bearer {token}"})
    print(response.json()['history'])

def test_create_group():
    response = requests.post(
        "http://"+ DAL_SVC_ADDRESS + "/group/create_group",
        headers={"Authorization": f"Bearer {token}"},
        params={"name": "testgroup", "description": "testdescription"}
    )
    print(response.status_code)
    print(response.json())

def test_enter_group():
    response = requests.get(
        "http://"+ DAL_SVC_ADDRESS + "/group/enter_group",
        headers={"Authorization": f"Bearer {token}"},
        params={"groupLink": "testgroup"}
    )
    print(response.status_code)
    print(response.json()["success"])

def test_accept_user():
    response = requests.post(
        "http://"+ DAL_SVC_ADDRESS + "/group/accept_user",
        headers={"Authorization": f"Bearer {token}"},
        params={"groupName": "testgroup", "username": "user3"}
    )
    print(response.json()["success"])

def test_leave_group():
    response = requests.delete(
        "http://"+ DAL_SVC_ADDRESS + "/group/leave_group",
        headers={"Authorization": f"Bearer {token}"},
        params={"groupName": "testgroup"}
    )
    print(response.json()["success"])

def test_remove_group():
    response = requests.delete(
        "http://"+ DAL_SVC_ADDRESS + "/group/remove_group",
        headers={"Authorization": f"Bearer {token}"},
        params={"groupName": "testgroup"}
    )
    print(response.json()["success"])

def test_add_password_to_group():
    response = requests.get(
        "http://"+ DAL_SVC_ADDRESS + "/group/addPassword",
        headers={"Authorization": f"Bearer {token}"},
        params={"groupName": "testgroup", "password": "testpassword11111", "name": "asdf", "shared": "True"}
    )
    print(response.json())

def test_remove_password_from_group():
    response = requests.get(
        "http://"+ DAL_SVC_ADDRESS + "/group/removePassword",
        headers={"Authorization": f"Bearer {token}"},
        params={"groupName": "testgroup", "passwordId": 1}
    )
    print(response.json()["success"])

def test_update_password_in_group():
    response = requests.get(
        "http://"+ DAL_SVC_ADDRESS + "/group/updPassword",
        headers={"Authorization": f"Bearer {token}"},
        params={"groupName": "testgroup", "passwordId": 1, "newPassword": "newpassword", "newName": "newname", "shared": "False"}
    )
    print(response.json()["success"])

def test_group_info():
    response = requests.get("http://"+ DAL_SVC_ADDRESS + "/group", params={"groupName": "testgroup"})
    print(response.json()['groupinfo'])

def test_logout():
    response = requests.delete("http://"+ DAL_SVC_ADDRESS + "/logout/", headers={"Authorization": f"Bearer {token}"})
    print(response.json()["success"])

def test_requests():
    header={"Authorization": f"Bearer {token}"}
    data = { "groupName" : "testgroup"}

    try:
        response = requests.get(
            f"http://{DAL_SVC_ADDRESS}/group/requests",headers=header , params=data
        )
        print(len(response.json()["requests"]))
        print(response.json()["requests"])
    except:
        print("Group not found")
    
def insertRequest(requestCommand):
    header={"Authorization": f"Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InExIiwiZW1haWwiOiJxMUAiLCJleHAiOjE3NDQ1NjE2MjN9.IwsnpQ1MeflnpfOroL6Xm-8omCckR4wHaSSaZXTjnTo"}

    data = { "groupName" : "testgroup", "requestCommand": requestCommand}

    response = requests.post(
            f"http://{DAL_SVC_ADDRESS}/group/insert_request",headers=header , params=data
        )

    print( response.json())
    
def acceptRequest():
    header={"Authorization": f"Bearer {token}"}

    data = { "groupName" : "testgroup", "requestId": 8}

    response = requests.post(
            f"http://{DAL_SVC_ADDRESS}/group/approve_request",headers=header , params=data
        )

    print( response.json())
    
def denyRequest():
    header={"Authorization": f"Bearer {token}"}

    data = { "groupName" : "testgroup", "requestId": 9}

    response = requests.delete(
            f"http://{DAL_SVC_ADDRESS}/group/deny_request",headers=header , params=data
        )

    print( response.json())

if __name__ == "__main__":
    login()
    #test_add_password()
    #test_get_user_passwords()
    #test_update_password()
    #test_get_user_passwords()
    test_delete_password()
    #test_get_user_passwords()
    #test_get_required_password()
    #test_history()
    #test_create_group()
    #test_enter_group()
    #insertRequest("ent{}")
    #test_requests()
    #test_accept_user()
    #test_leave_group()
    #test_remove_group()
    #test_create_group()#
    #test_add_password_to_group()
    #test_remove_password_from_group()
    #test_update_password_in_group()
    #test_add_password_to_group()
    #test_group_info()
    #test_logout()
    #print("All tests passed")
    #test_requests()
    #insertRequest("ent{}")
    #insertRequest("add{'password': 'testpassword', 'name': 'testname', 'shared': 'True'}")    
    #insertRequest("add{'password': 'testpassword3', 'name': 'testname3', 'shared': 'True'}")    
    #insertRequest("del{'passwordId': 1}")
    #print("deny request")
    #denyRequest()
    #acceptRequest()
    #test_requests()
