import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from common.base import Base, engine
from server import server, getCurrentUser, db

# Create a test database engine
#SQLALCHEMY_DATABASE_URL = "sqlite:///projectdb1.db"
#engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override the database dependency
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

server.dependency_overrides[getCurrentUser] = override_get_db

client = TestClient(server)

@pytest.fixture(scope="module")
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_add_password(setup_database):
    response = client.post(
        "/changes/add/",
        headers={"Authorization": "Bearer testtoken"},
        json={"password": "testpassword", "name": "testname", "shared": "False"}
    )
    assert response.status_code == 200
    assert response.json() == {"success", 200}

def test_update_password(setup_database):
    response = client.post(
        "/changes/update/",
        headers={"Authorization": "Bearer testtoken"},
        json={"currPasswordId": 1, "newPassword": "newpassword", "newName": "newname", "shared": "False"}
    )
    assert response.status_code == 200
    assert response.json() == {"success", 200}

def test_delete_password(setup_database):
    response = client.delete(
        "/changes/delete/",
        headers={"Authorization": "Bearer testtoken"},
        json={"currPasswordId": 1}
    )
    assert response.status_code == 200
    assert response.json() == {"success", 200}

def test_get_required_password(setup_database):
    response = client.get("/getPassword", params={"passwordId": 1})
    assert response.status_code == 200
    assert "password" in response.json()

def test_get_user_passwords(setup_database):
    response = client.get("/getPasswords", headers={"Authorization": "Bearer testtoken"})
    assert response.status_code == 200
    assert "passwords" in response.json()

def test_history(setup_database):
    response = client.get("/history", headers={"Authorization": "Bearer testtoken"})
    assert response.status_code == 200
    assert "history" in response.json()

def test_create_group(setup_database):
    response = client.post(
        "/group/create_group",
        headers={"Authorization": "Bearer testtoken"},
        json={"name": "testgroup", "description": "testdescription"}
    )
    assert response.status_code == 200
    assert response.json() == {"success", 200}

def test_enter_group(setup_database):
    response = client.get(
        "/group/enter_group",
        headers={"Authorization": "Bearer testtoken"},
        params={"groupLink": "testgroup123456"}
    )
    assert response.status_code == 200
    assert response.json() == {"success", 200}

def test_accept_user(setup_database):
    response = client.post(
        "/group/accept_user",
        headers={"Authorization": "Bearer testtoken"},
        json={"groupName": "testgroup"}
    )
    assert response.status_code == 200
    assert response.json() == {"success", 200}

def test_leave_group(setup_database):
    response = client.delete(
        "/group/leave_group",
        headers={"Authorization": "Bearer testtoken"},
        json={"groupName": "testgroup"}
    )
    assert response.status_code == 200
    assert response.json() == {"success", 200}

def test_remove_group(setup_database):
    response = client.delete(
        "/group/remove_group",
        headers={"Authorization": "Bearer testtoken"},
        json={"groupName": "testgroup"}
    )
    assert response.status_code == 200
    assert response.json() == {"success", 200}

def test_add_password_to_group(setup_database):
    response = client.get(
        "/group/addPassword",
        headers={"Authorization": "Bearer testtoken"},
        params={"groupName": "testgroup", "password": "testpassword", "name": "testname", "shared": "False"}
    )
    assert response.status_code == 200
    assert response.json() == {"success", 200}

def test_remove_password_from_group(setup_database):
    response = client.get(
        "/group/removePassword",
        headers={"Authorization": "Bearer testtoken"},
        params={"groupName": "testgroup", "passwordId": 1}
    )
    assert response.status_code == 200
    assert response.json() == {"success", 200}

def test_update_password_in_group(setup_database):
    response = client.get(
        "/group/updPassword",
        headers={"Authorization": "Bearer testtoken"},
        params={"groupName": "testgroup", "passwordId": 1, "newPassword": "newpassword", "newName": "newname", "shared": "False"}
    )
    assert response.status_code == 200
    assert response.json() == {"success", 200}

def test_group_info(setup_database):
    response = client.get("/group", params={"groupName": "testgroup"})
    assert response.status_code == 200
    assert "name" in response.json()

def test_logout(setup_database):
    response = client.delete("/logout/", headers={"Authorization": "Bearer testtoken"})
    assert response.status_code == 200
    assert response.json() == {"success", 200}