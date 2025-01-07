from flask import Flask, request
import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from ..storage.notification import Notification
from common.base import session_factory

server = Flask(__name__)
HOST = 'smtp.gmail.com'
PORT = 587

@server.route("/send_msg", methods=["POST"])
def sendNotification():
    #fromDepartment = request.form.get('from_department')
    doctorsEmail = request.form.get('from_doctor')
    #toDepartment = request.form.get('to_department')
    toDoctor = request.form.get('to_doctor')
    msgToSend = request.form.get('data')

    fromEmail = 'princessaaaa96@gmail.com'
    password = 'bdin qfib scdq kwzn'

    #bdin qfib scdq kwzn
    # Create message container
    msg = MIMEMultipart()
    msg['From'] = fromEmail
    msg['To'] = toDoctor
    msg['Subject'] = msgToSend

    # Attach the body with the msg instance
    msg.attach(MIMEText(msgToSend, 'plain'))

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
        server.sendmail(fromEmail, toDoctor, text)  # Send the email
        print("Email sent successfully")
        insertNotification(Notification('1', doctorsEmail, '2',toDoctor, msgToSend))
        getNotifications()
        server.quit()
        return 'True' ,200
    except Exception as e:
        print(f"Failed to send email: {e}")
        return 'False', 400

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
    server.run(host='127.0.0.1', port=2343)