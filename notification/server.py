from fastapi import FastAPI, Request, HTTPException, Depends
import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from typing import Annotated
import os, sys, jwt, random
sys.path.append(os.path.abspath('..'))
from common.classes import Requestt as r
from common.classes import Notification, User
from common.base import session_factory, _SessionFactory
from sqlalchemy import insert

server = FastAPI()
session_factory()
server.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
oauth2Schema = OAuth2PasswordBearer(tokenUrl="placeholder")

HOST = 'smtp.gmail.com'
PORT = 587
fromEmail = 'princessaaaa96@gmail.com'
password = 'jocg vnra ltyu ksuj'

@server.post("/sendAuthentication/")
def sendNotification(request: Request, token: Annotated[str, Depends(oauth2Schema)]):
    user = jwt.decode(token, "SARCASM", algorithms=["HS256"])["email"]
    generatedCode = str(random.randint(100000, 999999))
    sended = send(fromEmail, user, "Authentication code", generatedCode)
    if sended:
       return {'generatedCode': generatedCode}
    else:
       raise HTTPException(status_code=500, detail="Failed to send email")
    
@server.post("/sendUpdate/")
def sendUpdate(request: Request, token: Annotated[str, Depends(oauth2Schema)], sender: str, receiver: str, data: str):
    sended = send(sender, receiver, "Update", data)
    if sended:
        return {"status": 200}
    else:
        raise HTTPException(status_code=500, detail="Failed to send email")
    
def send(sender, to, subject, body) -> bool:
    context = ssl.create_default_context()
    try:
        # Set up the server using Gmail's SMTP server
        server = smtplib.SMTP(HOST, PORT)
        statusCode, response = server.ehlo()
        statusCode, response = server.starttls()  # Upgrade the connection to a secure encrypted SSL/TLS connection
        statusCode, response = server.login(fromEmail, password)  # Login to the email server
        text = createMsgContainer(sender, to, subject, body).as_string()  # Convert the message to a string
        server.sendmail(fromEmail, to, text)  # Send the email
        insertNotification( sender, to, subject, body)
        server.quit()
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False
    
def createMsgContainer(sender, to, subject, body):
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = to
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    return msg

def insertNotification(sender, to, subject, body):
    senderr = getUser(sender) if subject == "Update" else sender
    session = _SessionFactory()
    insert_stmt = insert(Notification).values(sender_id=senderr, reciever_id=getUser(to).id, data=subject + "-" + body)
    session.execute(insert_stmt)
    session.commit()
    session.close()

def getUser(email):
    db = _SessionFactory()
    return (db.query(User).filter(User.email == email).all())[0]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(server, host="182.20.1.6", port=5003)