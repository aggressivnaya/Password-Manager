import requests
from fastapi import HTTPException, Request
import os
import sys
sys.path.append(os.path.abspath('..'))
from common.base import _SessionFactory, session_factory
from common.classes import User

DAL_SVC_ADDRESS = '182.20.1.4:5001'

def isExist( username, email) -> bool:
    db = _SessionFactory()
    user = (db.query(User).filter(User.username == 'user1').all())[0]
    print(user.username + " " + user.email)
    return user