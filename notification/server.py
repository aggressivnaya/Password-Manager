from fastapi import FastAPI, Request, HTTPException, Depends
import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from typing import Annotated
import os, sys, jwt, random
sys.path.append(os.path.abspath('..'))
from common.classes import Request as r
from common.base import session_factory

server = FastAPI()
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
password = 'bdin qfib scdq kwzn'

@server.post("/sendAuthentication/")
def sendNotification(request: Request, token: Annotated[str, Depends(oauth2Schema)]):
    user = jwt.decode(request.headers.get("Authorization").split(' ')[1], "SARCASM", algorithms=["HS256"])['name']
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
        return {"status": "Email sent successfully"}
    else:
        raise HTTPException(status_code=500, detail="Failed to send email")
    
def send(sender, to, subject, body) -> bool:
    context = ssl.create_default_context()
    try:
        # Set up the server using Gmail's SMTP server
        server = smtplib.SMTP(HOST, PORT)
        statusCode, response = server.ehlo()
        print(f'Echoing the server: {statusCode} {response}')
        statusCode, response = server.starttls()  # Upgrade the connection to a secure encrypted SSL/TLS connection
        print(f'Starting TLS connection: {statusCode} {response}')
        #server.ehlo()
        statusCode, response = server.login(fromEmail, password)  # Login to the email server
        print(f'Loggin in: {statusCode} {response}')
        text = createMsgContainer(sender, to, subject, body).as_string()  # Convert the message to a string
        server.sendmail(fromEmail, to, text)  # Send the email
        print("Email sent successfully")
        insertNotification(r('1', sender, '2',to, body))
        getNotifications()
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

def insertNotification(notification):
    session = session_factory()
    session.add(notification)
    session.commit()
    session.close()
    
def getNotifications():
    session = session_factory()
    notificationQuery = session.query(r)
    session.close()
    n1 = notificationQuery.all()
    for n in n1:
        print(f"from {n.fromDepartment} ,{n.fromDoctor} to {n.toDepartment}, {n.toDoctor} data {n.data}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(server, host="182.20.1.6", port=5003)