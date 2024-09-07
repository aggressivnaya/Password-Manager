import socket
import select
import database as db
import requestHandler as rh

LISTEN_PORT = 90

def convertRecievedMsg(msg) -> rh.RequestInfo:
    '''
    getting the request from the client and converting to RequestInfo
    '''
    splittedMsg = msg.split('[')
    requestId = int(splittedMsg[0])
    request = splittedMsg[1].replace(']', '')
    print(f"requestId: {requestId}, request: {request}")
    return rh.RequestInfo(requestId, request)

def convertToSend(requestResult) -> str:
    msgToSend = str(requestResult.requestId) + "[" + requestResult.response + "]" 
    print(msgToSend)
    return msgToSend
    

class Server:
    def __init__(self) -> None:
        self.__db = db.Database()
        self.__sockets = {}
    
    def run(self) -> None:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                server_address = ('', LISTEN_PORT)
                sock.bind(server_address)
                sock.listen(5)
                sockets = [sock]

                while True:
                    # Wait for at least one of the sockets to be ready for processing
                    readable, writable, exceptional = select.select(sockets, [], [])
                    
                    for s in readable:
                        client_soc = None
                        client_address = None
                        if s is sock:
                            # If the server socket is readable, it means a new client is trying to connect
                            client_soc, client_address = s.accept()
                            print(f"New connection from {client_address}")
                            self.__sockets[client_soc] = rh.LoginRequestHandler(self.__db)
                            sockets.append(client_soc)
                            
                        else:
                            # Handle data from the connected clients
                            msg = s.recv(1024).decode()
                            print(f"Received data: {msg} from {s.getpeername()}")
                            if msg:
                                requestInfo = convertRecievedMsg(msg)
                                
                                handler = self.__sockets[s]
                                if handler.isRequestRelevant(requestInfo.requestId):
                                    #print(f"request is relevant to handler:{type(handler)}")
                                    requestResult = handler.handleRequest(requestInfo)
                                    s.sendall(convertToSend(requestResult).encode())
                                    if requestInfo.requestId == rh.Request.LOGOUT.value:
                                        self.closeSocket(sockets, s)
                                        continue
                                    else:
                                        self.__sockets[s] = requestResult.newHandler
                            else:
                                # If no data is received, the client has closed the connection
                                self.closeSocket(sockets, s)                              
        except Exception as e:
            print(e)
            self.closeSocket(sockets, s)
        except KeyboardInterrupt as key:
            print(key)

    def closeSocket(self, sockets ,s):
        print(f"Closing connection to {s.getpeername()}")
        sockets.remove(s)
        self.__sockets.pop(s)
        s.close()

if __name__ == "__main__":
    server = Server()
    server.run()