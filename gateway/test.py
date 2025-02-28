import pytest
from fastapi.testclient import TestClient
from gateway.server import server

client = TestClient(server)

def test_login():
    response = client.post("/login", json={"name": "testuser", "email": "test@example.com"})
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_signup():
    response = client.post("/signup", json={"name": "newuser", "email": "new@example.com"})
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_check():
    response = client.get("/check", params={"code": "123456"})
    assert response.status_code == 200

def test_passwords():
    response = client.get("/passwords", params={"passwordId": 1})
    assert response.status_code == 200

def test_password_add():
    response = client.post("/passwords/add", json={"password": "password123", "name": "testpassword", "shared": "no"})
    assert response.status_code == 200

def test_password_update():
    response = client.post("/passwords/update", json={"currPasswordId": 1, "newPassword": "newpassword123", "newName": "newtestpassword", "shared": "yes"})
    assert response.status_code == 200

def test_password_delete():
    response = client.post("/passwords/delete", json={"currPasswordId": 1})
    assert response.status_code == 200

def test_groups():
    response = client.get("/groups", params={"groupName": "testgroup"})
    assert response.status_code == 200

def test_group_passwords():
    response = client.get("/groups/testgroup/passwords")
    assert response.status_code == 200

def test_group_password_add():
    response = client.post("/groups/testgroup/passwords/add", json={"password": "password123", "name": "testpassword", "shared": "no"})
    assert response.status_code == 200

def test_history():
    response = client.get("/history")
    assert response.status_code == 200

def test_logout():
    response = client.get("/logout")
    assert response.status_code == 200