import socket
import select
import database as db
import requestHandler as rh

LISTEN_PORT = 90

def convertRecievedMsg(msg) -> rh.RequestInfo:
    splittedMsg = msg.split('[')
    requestId = int(splittedMsg[0])
    request = splittedMsg[1].replace(']', '')
    print(f"requestId: {requestId}, request: {request}")
    return rh.RequestInfo(requestId, request)

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
                            print("LoginRequestHandler initialized")
                            
                        else:
                            # Handle data from the connected clients
                            msg = s.recv(1024).decode()
                            print(f"Received data: {msg} from {s.getpeername()}")
                            if msg:
                                requestInfo = convertRecievedMsg(msg)
                                
                                if requestInfo.requestId == rh.Request.LOGOUT.value:
                                    print(f"Closing connection to {s.getpeername()}")
                                    self.__sockets.remove(s)
                                    s.close()
                                    continue
                                
                                print("going to check if the requestid is relevant")
                                handler = self.__sockets[s]
                                print(f"handler type: {type(handler)}")
                                #need a lot of time to do this if
                                if handler.isRequestRelevant(requestInfo.requestId):
                                    print(f"request is relevant to handler:{type(handler)}")
                                    requestResult = handler.handleRequest(requestInfo)
                                    print(type(requestResult))
                                    print("getted request result")
                                    print(requestResult.requestId)
                                    if requestResult.requestId == rh.Response.ERROR.value:
                                        raise Exception("new handler is none")
                                    
                                    print(requestResult.response)
                                    s.sendall(requestResult.response.encode())
                                    self.__sockets[s] = requestResult.newHandler
                            else:
                                # If no data is received, the client has closed the connection
                                print(f"Closing connection to {s.getpeername()}")
                                sockets.remove(s)
                                del self.__sockets[s]
                                s.close()
        except Exception as e:
            print(e)

def main():
    server = Server()
    server.run()

if __name__ == "__main__":
    main()