#import pytest
#from fastapi.testclient import TestClient
#from sqlalchemy import create_engine
#from sqlalchemy.orm import sessionmaker
#from auth.server import server, db, User, createToken
#from common.base import Base, engine
import os, requests

AUTH_SVC_ADDRESS = '182.20.1.3:5000'
#AUTH_SVC_ADDRESS = '127.0.0.1:5000'

def login(name, email):
    data = {
    "username": name,
    "email": email,
    }
    try:
        response = requests.post(
            f"http://{AUTH_SVC_ADDRESS}/login/", json=data
        )
        print(response.json()['access_token'])
    except Exception as e:
        print(e)
    
def signup( name ,email):
    data = {
    "username": name,
    "email": email,
    }
    try:
        response = requests.post(
            f"http://{AUTH_SVC_ADDRESS}/signup/", json=data
        )
        print(response.json()['access_token'])
    except Exception as e:
        print(e)

if __name__ == "__main__":
    signup("user33", "1asdf111")
    #login("user1", "user1@example.com")
