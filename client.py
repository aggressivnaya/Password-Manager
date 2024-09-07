import socket
import requestHandler as rh
from enum import Enum

SERVER_ADDRESS = '127.0.0.1'
SERVER_PORT = 90

class Messsages(Enum): 
    LOGIN = '101[alice,123]'
    SIGNUP = '102[alice,123,alice@]'
    LOGOUT = '107[alice]'
    ADDPASSWORD = '103[1415]'
    GETPASSWORDS = '106[alice]'
    UPDATEPASSWORD = '104[123415,12]'
    DELETEPASSWORD = '105[1415]'

def msgs(i) -> str:
    if i == 1:
        return Messsages.LOGIN.value
    elif i == 6:
        return Messsages.ADDPASSWORD.value
    elif i == 3:
        return Messsages.DELETEPASSWORD.value
    elif i == 5:
        return Messsages.UPDATEPASSWORD.value
    elif i == 2:
        return Messsages.GETPASSWORDS.value
    elif i == 4:
        return Messsages.LOGOUT.value

def main():
    i = 1
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            sock.connect((SERVER_ADDRESS, SERVER_PORT))
            print(f"Connected to server at {SERVER_ADDRESS}:{SERVER_PORT}")

            while i < 5:
                # Send a message to the server
                message = msgs(i)
                print(f"Sending message: {message}")
                sock.sendall(message.encode())

                # Receive the response from the server
                response = sock.recv(1024).decode()
                print(f"Received response: {response}")
                i += 1
        except Exception as e:
            print(f"Error: {e}")

    

if __name__ == "__main__":
    main()
