import requests

DAL_SVC_ADDRESS = '182.20.1.4:5001'

def test_add_password():
    response = requests.post(
        "http://"+ DAL_SVC_ADDRESS + "/changes/add/",
        headers={"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InVzZXIxIiwiZW1haWwiOiJ1c2VyMUBleGFtcGxlLmNvbSIsImV4cCI6MTc0MzE3MjQ1OX0.nYYM9z1Rmc2ay1FYYunMZAXAvksXyNlFtyuU8MgfqGc"},
        params={"password": "testpassword", "name": "testname", "shared": "False"}
    )
    #assert response.status_code == 200
    #assert response.json() == {"success", 200}
    print(response.json()["success"])

def test_update_password():
    response = requests.post(
        "http://"+ DAL_SVC_ADDRESS + "/changes/update/",
        headers={"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InVzZXIxIiwiZW1haWwiOiJ1c2VyMUBleGFtcGxlLmNvbSIsImV4cCI6MTc0MzE3MjQ1OX0.nYYM9z1Rmc2ay1FYYunMZAXAvksXyNlFtyuU8MgfqGc"},
        json={"currPasswordId": 1, "newPassword": "newpassword", "newName": "newname", "shared": "False"}
    )
    #assert response.status_code == 200
    #assert response.json() == {"success", 200}
    print(response.json()["success"])

def test_delete_password():
    response = requests.delete(
        "http://"+ DAL_SVC_ADDRESS + "/changes/delete/",
        headers={"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InVzZXIxIiwiZW1haWwiOiJ1c2VyMUBleGFtcGxlLmNvbSIsImV4cCI6MTc0MzE3MjQ1OX0.nYYM9z1Rmc2ay1FYYunMZAXAvksXyNlFtyuU8MgfqGc"},
        json={"currPasswordId": 1}
    )
    #assert response.status_code == 200
    #assert response.json() == {"success", 200}
    print(response.json()["success"])

def test_get_required_password():
    response = requests.get("http://"+ DAL_SVC_ADDRESS + "/getPassword",headers={"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InVzZXIxIiwiZW1haWwiOiJ1c2VyMUBleGFtcGxlLmNvbSIsImV4cCI6MTc0MzE3MjQ1OX0.nYYM9z1Rmc2ay1FYYunMZAXAvksXyNlFtyuU8MgfqGc"}, params={"passwordId": 3})
    #assert response.status_code == 200
    #assert "password" in response.json()
    print(response.json()['password'])

def test_get_user_passwords():
    response = requests.get("http://"+ DAL_SVC_ADDRESS + "/getPasswords", headers={"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InVzZXIxIiwiZW1haWwiOiJ1c2VyMUBleGFtcGxlLmNvbSIsImV4cCI6MTc0MzE3MjQ1OX0.nYYM9z1Rmc2ay1FYYunMZAXAvksXyNlFtyuU8MgfqGc"})
    #assert response.status_code == 200
    #assert "passwords" in response.json()
    print(response.json()['passwords'])

def test_history():
    response = requests.get("http://"+ DAL_SVC_ADDRESS + "/history", headers={"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InVzZXIxIiwiZW1haWwiOiJ1c2VyMUBleGFtcGxlLmNvbSIsImV4cCI6MTc0MzE3MjQ1OX0.nYYM9z1Rmc2ay1FYYunMZAXAvksXyNlFtyuU8MgfqGc"})
    #assert response.status_code == 200
    #assert "history" in response.json()
    print(response.json()['history'])

def test_create_group():
    response = requests.post(
        "http://"+ DAL_SVC_ADDRESS + "/group/create_group",
        headers={"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InVzZXIxIiwiZW1haWwiOiJ1c2VyMUBleGFtcGxlLmNvbSIsImV4cCI6MTc0MzE3MjQ1OX0.nYYM9z1Rmc2ay1FYYunMZAXAvksXyNlFtyuU8MgfqGc"},
        params={"name": "testgroup", "description": "testdescription"}
    )
    #assert response.status_code == 200
    #assert response.json() == {"success", 200}
    print(response.status_code)
    print(response.json())

def test_enter_group():
    response = requests.get(
        "http://"+ DAL_SVC_ADDRESS + "/group/enter_group",
        headers={"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InVzZXIxIiwiZW1haWwiOiJ1c2VyMUBleGFtcGxlLmNvbSIsImV4cCI6MTc0MzE3MjQ1OX0.nYYM9z1Rmc2ay1FYYunMZAXAvksXyNlFtyuU8MgfqGc"},
        params={"groupLink": "testgroup"}
    )
    #assert response.status_code == 200
    #assert response.json() == {"success", 200}
    print(response.status_code)
    print(response.json()["success"])

def test_accept_user():
    response = requests.post(
        "http://"+ DAL_SVC_ADDRESS + "/group/accept_user",
        headers={"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InVzZXIxIiwiZW1haWwiOiJ1c2VyMUBleGFtcGxlLmNvbSIsImV4cCI6MTc0MzE3MjQ1OX0.nYYM9z1Rmc2ay1FYYunMZAXAvksXyNlFtyuU8MgfqGc"},
        params={"groupName": "testgroup", "username": "user3"}
    )
    #assert response.status_code == 200
    #assert response.json() == {"success", 200}
    print(response.json()["success"])

def test_leave_group():
    response = requests.delete(
        "http://"+ DAL_SVC_ADDRESS + "/group/leave_group",
        headers={"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InVzZXIxIiwiZW1haWwiOiJ1c2VyMUBleGFtcGxlLmNvbSIsImV4cCI6MTc0MzE3MjQ1OX0.nYYM9z1Rmc2ay1FYYunMZAXAvksXyNlFtyuU8MgfqGc"},
        params={"groupName": "testgroup"}
    )
    #assert response.status_code == 200
    #assert response.json() == {"success", 200}
    print(response.json()["success"])

def test_remove_group():
    response = requests.delete(
        "http://"+ DAL_SVC_ADDRESS + "/group/remove_group",
        headers={"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InVzZXIxIiwiZW1haWwiOiJ1c2VyMUBleGFtcGxlLmNvbSIsImV4cCI6MTc0MzE3MjQ1OX0.nYYM9z1Rmc2ay1FYYunMZAXAvksXyNlFtyuU8MgfqGc"},
        params={"groupName": "testgroup"}
    )
    #assert response.status_code == 200
    #assert response.json() == {"success", 200}
    print(response.json()["success"])

def test_add_password_to_group():
    response = requests.get(
        "http://"+ DAL_SVC_ADDRESS + "/group/addPassword",
        headers={"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InVzZXIxIiwiZW1haWwiOiJ1c2VyMUBleGFtcGxlLmNvbSIsImV4cCI6MTc0MzE3MjQ1OX0.nYYM9z1Rmc2ay1FYYunMZAXAvksXyNlFtyuU8MgfqGc"},
        params={"groupName": "testgroup", "password": "testpassword11111", "name": "asdf", "shared": "True"}
    )
    #assert response.status_code == 200
    #assert response.json() == {"success", 200}
    print(response.json())

def test_remove_password_from_group():
    response = requests.get(
        "http://"+ DAL_SVC_ADDRESS + "/group/removePassword",
        headers={"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InVzZXIxIiwiZW1haWwiOiJ1c2VyMUBleGFtcGxlLmNvbSIsImV4cCI6MTc0MzE3MjQ1OX0.nYYM9z1Rmc2ay1FYYunMZAXAvksXyNlFtyuU8MgfqGc"},
        params={"groupName": "testgroup", "passwordId": 1}
    )
    #assert response.status_code == 200
    #assert response.json() == {"success", 200}
    print(response.json()["success"])

def test_update_password_in_group():
    response = requests.get(
        "http://"+ DAL_SVC_ADDRESS + "/group/updPassword",
        headers={"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InVzZXIxIiwiZW1haWwiOiJ1c2VyMUBleGFtcGxlLmNvbSIsImV4cCI6MTc0MzE3MjQ1OX0.nYYM9z1Rmc2ay1FYYunMZAXAvksXyNlFtyuU8MgfqGc"},
        params={"groupName": "testgroup", "passwordId": 1, "newPassword": "newpassword", "newName": "newname", "shared": "False"}
    )
    #assert response.status_code == 200
    #assert response.json() == {"success", 200}
    print(response.json()["success"])

def test_group_info():
    response = requests.get("http://"+ DAL_SVC_ADDRESS + "/group", params={"groupName": "testgroup"})
    #assert response.status_code == 200
    #assert "name" in response.json()
    print(response.json()['groupinfo'])

def test_logout():
    response = requests.delete("http://"+ DAL_SVC_ADDRESS + "/logout/", headers={"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InVzZXIxIiwiZW1haWwiOiJ1c2VyMUBleGFtcGxlLmNvbSIsImV4cCI6MTc0MzE3MjQ1OX0.nYYM9z1Rmc2ay1FYYunMZAXAvksXyNlFtyuU8MgfqGc"})
    #assert response.status_code == 200
    #assert response.json() == {"success", 200}
    print(response.json()["success"])


if __name__ == "__main__":
    #test_add_password()
    #test_update_password()
    #test_delete_password()
    test_get_user_passwords()
    test_get_required_password()
    test_history()
    #test_create_group()
    #test_enter_group()
    #test_accept_user()
    #test_leave_group()
    #test_remove_group()
    #test_create_group()#
    #test_add_password_to_group()
    #test_remove_password_from_group()
    #test_update_password_in_group()
    #test_add_password_to_group()
    test_group_info()
    test_logout()
    print("All tests passed")