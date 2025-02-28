import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from auth.server import server, db, User, createToken
from common.base import Base, engine

client = TestClient(server)

# Create a test database
#SQLALCHEMY_DATABASE_URL = "sqlite:///projectdb1.db"
#engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="module")
def test_db():
    db = TestingSessionLocal()
    yield db
    db.close()

@pytest.fixture(scope="module")
def client_with_db(test_db):
    server.dependency_overrides[db] = lambda: test_db
    yield client
    server.dependency_overrides = {}

def test_signup(client_with_db):
    response = client_with_db.post("/signup/", json={"name": "testuser", "email": "testuser@example.com"})
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login(client_with_db):
    response = client_with_db.post("/login/", json={"name": "testuser", "email": "testuser@example.com"})
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_invalid_credentials(client_with_db):
    response = client_with_db.post("/login/", json={"name": "invaliduser", "email": "invalid@example.com"})
    assert response.status_code == 401
    assert response.json() == {"detail": "invalid credentials"}

def test_validate(client_with_db):
    token = createToken("testuser", "testuser@example.com")
    headers = {"Authorization": f"Bearer {token}"}
    response = client_with_db.post("/validate/", headers=headers)
    assert response.status_code == 200
    assert response.json() == {"validated": True}

def test_validate_invalid_token(client_with_db):
    headers = {"Authorization": "Bearer invalidtoken"}
    response = client_with_db.post("/validate/", headers=headers)
    assert response.status_code == 401
    assert response.json() == {"detail": "not authorized"}