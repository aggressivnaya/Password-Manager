import socket
import RequestHandler as rh
from enum import Enum

SERVER_ADDRESS = '127.0.0.1'
SERVER_PORT = 90

class Messsages(Enum): 
    LOGIN = '101[]'
    SIGNUP = '102[alice,123,alice@]'
    LOGOUT = '107[alice]'
    ADDPASSWORD = '103[12345]'
    GETPASSWORDS = '106[alice]'

def msgs(i) -> str:
    if i == 1:
        return Messsages.LOGIN.value
    elif i == 2:
        return Messsages.SIGNUP.value
    elif i == 3:
        return Messsages.ADDPASSWORD.value
    elif i == 4:
        return Messsages.GETPASSWORDS.value
    elif i == 5:
        return Messsages.LOGOUT.value

def main():
    i = 2
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((SERVER_ADDRESS, SERVER_PORT))
        response = sock.recv(1024)
        while i != 5:
            message = msgs(i)
            print(message)
            sock.sendall(message.encode())
            response = sock.recv(1024)
            print(f"Received response: {response.decode()}")
            i += 1
    

if __name__ == "__main__":
    main()
