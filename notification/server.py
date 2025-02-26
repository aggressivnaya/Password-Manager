from fastapi import FastAPI
import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import sys
sys.path.append(os.path.abspath('..'))
from dal.classes.notificationDb import Notification
from common.base import session_factory

server = FastAPI()
HOST = 'smtp.gmail.com'
PORT = 587
fromEmail = 'princessaaaa96@gmail.com'
password = 'bdin qfib scdq kwzn'

@server.post("/send_msg/")
def sendNotification(sender: str, to: str, subject: str, body: str):
    #bdin qfib scdq kwzn
    # Create message container
    msg = MIMEMultipart()
    msg['From'] = fromEmail
    msg['To'] = to
    msg['Subject'] = subject

    # Attach the body with the msg instance
    msg.attach(MIMEText(body, 'plain'))

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
        text = msg.as_string()  # Convert the message to a string
        server.sendmail(fromEmail, to, text)  # Send the email
        print("Email sent successfully")
        insertNotification(Notification('1', sender, '2',to, body))
        getNotifications()
        server.quit()
        return {'sended': 'True'}
    except Exception as e:
        print(f"Failed to send email: {e}")
        return {'sended': 'False'}

def insertNotification(notification):
    session = session_factory()
    session.add(notification)
    session.commit()
    session.close()
    
def getNotifications():
    session = session_factory()
    notificationQuery = session.query(Notification)
    session.close()
    n1 = notificationQuery.all()
    for n in n1:
        print(f"from {n.fromDepartment} ,{n.fromDoctor} to {n.toDepartment}, {n.toDoctor} data {n.data}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(server, host="182.20.1.6", port=5003)