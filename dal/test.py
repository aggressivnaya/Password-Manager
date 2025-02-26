import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from dal.server import server, getCurrentUser

# FILE: dal/test_server.py


client = TestClient(server)

# Mock getCurrentUser function
def mock_getCurrentUser(token):
    return MagicMock(id=1, username="user1")

@patch('dal.server.getCurrentUser', side_effect=mock_getCurrentUser)
def test_addPassword(mock_getCurrentUser):
    response = client.post("/changes/add/", headers={"Authorization": "Bearer testtoken"}, json={"password": "testpass", "name": "testname", "shared": "false"})
    assert response.status_code == 200
    assert response.json() == {"success", 200}

@patch('dal.server.getCurrentUser', side_effect=mock_getCurrentUser)
def test_updatePassword(mock_getCurrentUser):
    response = client.post("/changes/update/", headers={"Authorization": "Bearer testtoken"}, json={"currPasswordId": 1, "newPassword": "newpass", "newName": "newname", "shared": "false"})
    assert response.status_code == 200
    assert response.json() == {"success", 200}

@patch('dal.server.getCurrentUser', side_effect=mock_getCurrentUser)
def test_deletePassword(mock_getCurrentUser):
    response = client.delete("/changes/delete/", headers={"Authorization": "Bearer testtoken"}, json={"currPasswordId": 1})
    assert response.status_code == 200
    assert response.json() == {"success", 200}

def test_getRequiredPassword():
    response = client.get("/getPassword", params={"passwordId": 1})
    assert response.status_code == 200
    assert "password" in response.json()

@patch('dal.server.getCurrentUser', side_effect=mock_getCurrentUser)
def test_getUserPasswords(mock_getCurrentUser):
    response = client.get("/getPasswords", headers={"Authorization": "Bearer testtoken"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@patch('dal.server.getCurrentUser', side_effect=mock_getCurrentUser)
def test_history(mock_getCurrentUser):
    response = client.get("/history", headers={"Authorization": "Bearer testtoken"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@patch('dal.server.getCurrentUser', side_effect=mock_getCurrentUser)
def test_createGroup(mock_getCurrentUser):
    response = client.post("/group/create_group", headers={"Authorization": "Bearer testtoken"}, json={"name": "testgroup", "description": "testdesc"})
    assert response.status_code == 200
    assert response.json() == {"success", 200}

@patch('dal.server.getCurrentUser', side_effect=mock_getCurrentUser)
def test_enterGroup(mock_getCurrentUser):
    response = client.get("/group/enter_group", headers={"Authorization": "Bearer testtoken"}, params={"groupLink": "testlink"})
    assert response.status_code == 200
    assert response.json() == {"success", 200}

@patch('dal.server.getCurrentUser', side_effect=mock_getCurrentUser)
def test_acceptUser(mock_getCurrentUser):
    response = client.post("/group/accept_user", headers={"Authorization": "Bearer testtoken"}, json={"username": "testuser", "group_name": "testgroup"})
    assert response.status_code == 200
    assert response.json() == {"success", 200}

@patch('dal.server.getCurrentUser', side_effect=mock_getCurrentUser)
def test_leaveGroup(mock_getCurrentUser):
    response = client.delete("/group/leave_group", headers={"Authorization": "Bearer testtoken"}, json={"groupName": "testgroup"})
    assert response.status_code == 200
    assert response.json() == {"success", 200}

@patch('dal.server.getCurrentUser', side_effect=mock_getCurrentUser)
def test_removeGroup(mock_getCurrentUser):
    response = client.delete("/group/remove_user", headers={"Authorization": "Bearer testtoken"}, json={"groupName": "testgroup"})
    assert response.status_code == 200
    assert response.json() == {"success", 200}

def test_groupInfo():
    response = client.get("/group", params={"groupName": "testgroup"})
    assert response.status_code == 200
    assert "name" in response.json()

@patch('dal.server.getCurrentUser', side_effect=mock_getCurrentUser)
def test_logout(mock_getCurrentUser):
    response = client.delete("/logout", headers={"Authorization": "Bearer testtoken"})
    assert response.status_code == 200
    assert response.json() == {"success", 200}