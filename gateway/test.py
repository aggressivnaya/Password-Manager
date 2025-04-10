import requests

GATEWAY_SVC_ADDRESS = '182.20.1.2:5002'
groupName = "testgroup456"

def test_add_password():
    response = requests.post(
        "http://"+ GATEWAY_SVC_ADDRESS + "/passwords/add",
        headers={"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InVzZXIxIiwiZW1haWwiOiJ1c2VyMUBleGFtcGxlLmNvbSIsImV4cCI6MTc0MzI1NjAzNH0.dKuGo1gEFS3TJ46kpw2Mk3L0PmHYHMAxsQoha2izvPM"},
        params={"password": "asd", "name": "a", "shared": "True"}
    )
    response = requests.post(
        "http://"+ GATEWAY_SVC_ADDRESS + "/passwords/add",
        headers={"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InVzZXIxIiwiZW1haWwiOiJ1c2VyMUBleGFtcGxlLmNvbSIsImV4cCI6MTc0MzI1NjAzNH0.dKuGo1gEFS3TJ46kpw2Mk3L0PmHYHMAxsQoha2izvPM"},
        params={"password": "ewer", "name": "d", "shared": "True"}
    )
    response = requests.post(
        "http://"+ GATEWAY_SVC_ADDRESS + "/passwords/add",
        headers={"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InVzZXIxIiwiZW1haWwiOiJ1c2VyMUBleGFtcGxlLmNvbSIsImV4cCI6MTc0MzI1NjAzNH0.dKuGo1gEFS3TJ46kpw2Mk3L0PmHYHMAxsQoha2izvPM"},
        params={"password": "cvb", "name": "f", "shared": "True"}
    )
    response = requests.post(
        "http://"+ GATEWAY_SVC_ADDRESS + "/passwords/add",
        headers={"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InVzZXIxIiwiZW1haWwiOiJ1c2VyMUBleGFtcGxlLmNvbSIsImV4cCI6MTc0MzI1NjAzNH0.dKuGo1gEFS3TJ46kpw2Mk3L0PmHYHMAxsQoha2izvPM"},
        params={"password": "ngf", "name": "r", "shared": "False"}
    )
    response = requests.post(
        "http://"+ GATEWAY_SVC_ADDRESS + "/passwords/add",
        headers={"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InVzZXIxIiwiZW1haWwiOiJ1c2VyMUBleGFtcGxlLmNvbSIsImV4cCI6MTc0MzI1NjAzNH0.dKuGo1gEFS3TJ46kpw2Mk3L0PmHYHMAxsQoha2izvPM"},
        params={"password": "testpassword", "name": "testname", "shared": "False"}
    )
    response = requests.post(
        "http://"+ GATEWAY_SVC_ADDRESS + "/passwords/add",
        headers={"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InVzZXIxIiwiZW1haWwiOiJ1c2VyMUBleGFtcGxlLmNvbSIsImV4cCI6MTc0MzI1NjAzNH0.dKuGo1gEFS3TJ46kpw2Mk3L0PmHYHMAxsQoha2izvPM"},
        params={"password": "testpassword123", "name": "testname123", "shared": "False"}
    )
    response = requests.post(
        "http://"+ GATEWAY_SVC_ADDRESS + "/passwords/add",
        headers={"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InVzZXIxIiwiZW1haWwiOiJ1c2VyMUBleGFtcGxlLmNvbSIsImV4cCI6MTc0MzI1NjAzNH0.dKuGo1gEFS3TJ46kpw2Mk3L0PmHYHMAxsQoha2izvPM"},
        params={"password": "testpassword456", "name": "testname456", "shared": "False"}
    )
    #assert response.status_code == 200
    #assert response.json() == {"success", 200}
    print(response.status_code, response.json())

def test_update_password():
    response = requests.post(
        "http://"+ GATEWAY_SVC_ADDRESS + "/passwords/update",
        headers={"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InVzZXIxIiwiZW1haWwiOiJ1c2VyMUBleGFtcGxlLmNvbSIsImV4cCI6MTc0MzI1NjAzNH0.dKuGo1gEFS3TJ46kpw2Mk3L0PmHYHMAxsQoha2izvPM"},
        json={"currPasswordId": 1, "newPassword": "newpassword", "newName": "newname", "shared": "False"}
    )
    #assert response.status_code == 200
    #assert response.json() == {"success", 200}
    print(response.status_code, response.json())

def test_delete_password():
    response = requests.delete(
        "http://"+ GATEWAY_SVC_ADDRESS + "/passwords/delete",
        headers={"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InVzZXIxIiwiZW1haWwiOiJ1c2VyMUBleGFtcGxlLmNvbSIsImV4cCI6MTc0MzI1NjAzNH0.dKuGo1gEFS3TJ46kpw2Mk3L0PmHYHMAxsQoha2izvPM"},
        json={"currPasswordId": 2}
    )
    #assert response.status_code == 200
    #assert response.json() == {"success", 200}
    print(response.status_code, response.json())

def test_get_required_password():
    response = requests.get("http://"+ GATEWAY_SVC_ADDRESS + "/getPassword",headers={"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InVzZXIxIiwiZW1haWwiOiJ1c2VyMUBleGFtcGxlLmNvbSIsImV4cCI6MTc0MzI1NjAzNH0.dKuGo1gEFS3TJ46kpw2Mk3L0PmHYHMAxsQoha2izvPM"}, params={"passwordId": 3})
    #assert response.status_code == 200
    #assert "password" in response.json()
    print(response.status_code, response.json()['password'])

def test_get_user_passwords():
    response = requests.get("http://"+ GATEWAY_SVC_ADDRESS + "/passwords", headers={"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InVzZXIxIiwiZW1haWwiOiJ1c2VyMUBleGFtcGxlLmNvbSIsImV4cCI6MTc0MzI1NjAzNH0.dKuGo1gEFS3TJ46kpw2Mk3L0PmHYHMAxsQoha2izvPM"})
    #assert response.status_code == 200
    #assert "passwords" in response.json()
    print(response.status_code, response.json())

def test_history():
    response = requests.get("http://"+ GATEWAY_SVC_ADDRESS + "/history", headers={"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InVzZXIxIiwiZW1haWwiOiJ1c2VyMUBleGFtcGxlLmNvbSIsImV4cCI6MTc0MzI1NjAzNH0.dKuGo1gEFS3TJ46kpw2Mk3L0PmHYHMAxsQoha2izvPM"})
    #assert response.status_code == 200
    #assert "history" in response.json()
    print(response.status_code, response.json())

def test_create_group():
    response = requests.post(
        "http://"+ GATEWAY_SVC_ADDRESS + f"/groups/{groupName}/createGroup",
        headers={"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InVzZXIxIiwiZW1haWwiOiJ1c2VyMUBleGFtcGxlLmNvbSIsImV4cCI6MTc0MzI1NjAzNH0.dKuGo1gEFS3TJ46kpw2Mk3L0PmHYHMAxsQoha2izvPM"},
        params={"name": "testgroup456", "description": "testdescription"}
    )
    #assert response.status_code == 200
    #assert response.json() == {"success", 200}

    print(response.status_code, response.json())

def test_enter_group():
    response = requests.post(
        "http://"+ GATEWAY_SVC_ADDRESS + f"/groups/{groupName}/enterGroup",
        headers={"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InVzZXIxIiwiZW1haWwiOiJ1c2VyMUBleGFtcGxlLmNvbSIsImV4cCI6MTc0MzI1NjAzNH0.dKuGo1gEFS3TJ46kpw2Mk3L0PmHYHMAxsQoha2izvPM"},
        params={"groupName": groupName}
    )
    #assert response.status_code == 200
    #assert response.json() == {"success", 200}
    
    print(response.status_code, response.json())

def test_accept_user():
    response = requests.post(
        "http://"+ GATEWAY_SVC_ADDRESS + f"/groups/{groupName}/acceptUser",
        headers={"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InVzZXIxIiwiZW1haWwiOiJ1c2VyMUBleGFtcGxlLmNvbSIsImV4cCI6MTc0MzI1NjAzNH0.dKuGo1gEFS3TJ46kpw2Mk3L0PmHYHMAxsQoha2izvPM"},
        params={"groupName": groupName, "username": "user3"}
    )
    #assert response.status_code == 200
    #assert response.json() == {"success", 200}
    print(response.status_code, response.json())

def test_leave_group():
    response = requests.delete(
        "http://"+ GATEWAY_SVC_ADDRESS + f"/groups/{groupName}/leaveGroup",
        headers={"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InVzZXIxIiwiZW1haWwiOiJ1c2VyMUBleGFtcGxlLmNvbSIsImV4cCI6MTc0MzI1NjAzNH0.dKuGo1gEFS3TJ46kpw2Mk3L0PmHYHMAxsQoha2izvPM"},
        params={"groupName": groupName}
    )
    #assert response.status_code == 200
    #assert response.json() == {"success", 200}
    print(response.status_code, response.json())

def test_remove_group():
    response = requests.delete(
        "http://"+ GATEWAY_SVC_ADDRESS + f"/groups/{groupName}/removeGroup",
        headers={"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InVzZXIxIiwiZW1haWwiOiJ1c2VyMUBleGFtcGxlLmNvbSIsImV4cCI6MTc0MzI1NjAzNH0.dKuGo1gEFS3TJ46kpw2Mk3L0PmHYHMAxsQoha2izvPM"},
        params={"groupName": groupName}
    )
    #assert response.status_code == 200
    #assert response.json() == {"success", 200}
    print(response.status_code, response.json())

def test_add_password_to_group():
    response = requests.post(
        "http://"+ GATEWAY_SVC_ADDRESS + f"/groups/{groupName}/passwords/add",
        headers={"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InVzZXIxIiwiZW1haWwiOiJ1c2VyMUBleGFtcGxlLmNvbSIsImV4cCI6MTc0MzI1NjAzNH0.dKuGo1gEFS3TJ46kpw2Mk3L0PmHYHMAxsQoha2izvPM"},
        params={"groupName": groupName, "password": "testpassword11111", "name": "asdf", "shared": "True"}
    )
    #assert response.status_code == 200
    #assert response.json() == {"success", 200}
    print(response.status_code, response.json())

def test_remove_password_from_group():
    response = requests.delete(
        "http://"+ GATEWAY_SVC_ADDRESS + f"/groups/{groupName}/passwords/delete",
        headers={"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InVzZXIxIiwiZW1haWwiOiJ1c2VyMUBleGFtcGxlLmNvbSIsImV4cCI6MTc0MzI1NjAzNH0.dKuGo1gEFS3TJ46kpw2Mk3L0PmHYHMAxsQoha2izvPM"},
        params={"groupName": groupName, "passwordId": 1}
    )
    #assert response.status_code == 200
    #assert response.json() == {"success", 200}
    print(response.status_code, response.json())

def test_update_password_in_group():
    response = requests.post(
        "http://"+ GATEWAY_SVC_ADDRESS + f"/groups/{groupName}/passwords/update",
        headers={"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InVzZXIxIiwiZW1haWwiOiJ1c2VyMUBleGFtcGxlLmNvbSIsImV4cCI6MTc0MzI1NjAzNH0.dKuGo1gEFS3TJ46kpw2Mk3L0PmHYHMAxsQoha2izvPM"},
        params={"groupName": groupName, "passwordId": 1, "newPassword": "newpassword", "newName": "newname", "shared": "False"}
    )
    #assert response.status_code == 200
    #assert response.json() == {"success", 200}
    print(response.status_code, response.json())

def test_get_groups():
    response = requests.get(
        "http://"+ GATEWAY_SVC_ADDRESS + "/groups",
        headers={"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InVzZXIxIiwiZW1haWwiOiJ1c2VyMUBleGFtcGxlLmNvbSIsImV4cCI6MTc0MzI1NjAzNH0.dKuGo1gEFS3TJ46kpw2Mk3L0PmHYHMAxsQoha2izvPM"},
    )
    #assert response.status_code == 200
    #assert response.json() == {"success", 200}
    print(response.status_code, response.json())

def test_group_info():
    response = requests.get("http://"+ GATEWAY_SVC_ADDRESS + f"/groups/{groupName}",headers={"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InVzZXIxIiwiZW1haWwiOiJ1c2VyMUBleGFtcGxlLmNvbSIsImV4cCI6MTc0MzI1NjAzNH0.dKuGo1gEFS3TJ46kpw2Mk3L0PmHYHMAxsQoha2izvPM"}, params={"groupName": groupName})
    #assert response.status_code == 200
    #assert "name" in response.json()
    print(response.status_code, response.json())

def test_logout():
    response = requests.delete("http://"+ GATEWAY_SVC_ADDRESS + "/logout/", headers={"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InVzZXIxIiwiZW1haWwiOiJ1c2VyMUBleGFtcGxlLmNvbSIsImV4cCI6MTc0MzI1NjAzNH0.dKuGo1gEFS3TJ46kpw2Mk3L0PmHYHMAxsQoha2izvPM"})
    #assert response.status_code == 200
    #assert response.json() == {"success", 200}
    print(response.status_code, response.json())


if __name__ == "__main__":
    payload = {
        "username": "user1",
        "email": "user1@example.com"
    }

    # Send POST request
    response = requests.post("http://127.0.0.1:5002/login", json=payload)

    # Print the response
    if response.status_code == 200:
        print("Login successful:", response.json())
    else:
        print("Login failed:", response.status_code, response.text)
    #test_add_password()
    #test_update_password()
    #test_delete_password()
    #test_get_user_passwords()
    #test_get_required_password()
    #test_history()
    #test_create_group()
    #test_enter_group()
    #test_accept_user()
    #test_leave_group()
    #
    #test_create_group()
    #test_add_password_to_group()
    #test_remove_password_from_group()
    #test_update_password_in_group()
    #test_add_password_to_group()
    #test_group_info()
    #test_get_groups()
    #test_remove_group()
    #test_logout()
    print("All tests passed")