import socket
import select
import RequestHandler as rh

LISTEN_PORT = 90
class Server:
    def __init__(self) -> None:
        self.__sockets = {}
        #self.__handlerFactory = 
        #self.__db = 
    
    def run(self) -> None:
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
                        self.__sockets[client_soc] = rh.LoginRequestHandler()
                    else:
                        # Handle data from the connected clients
                        msg = s.recv(1024).decode()
                        print(f"Received data: {msg} from {s.getpeername()}")
                        if msg:
                            requestInfo = convertRecievedMsg(msg)
                            self.__sockets[client_soc].setUser = requestInfo.request.split(' ')[0]#getting username
                            handler = self.__sockets[client_soc]
                            if handler.isRequestRelevant(requestInfo.requestId):
                                requestResult = handler.handlerRequest(requestInfo.requestId)
                                s.sendall(msg)
                                self.__sockets[client_soc] = requestResult.newHandler
                        else:
                            # If no data is received, the client has closed the connection
                            print(f"Closing connection to {s.getpeername()}")
                            self.__sockets.remove(s)
                            s.close()

def convertRecievedMsg(msg) -> rh.RequestInfo:
    splittedMsg =  msg.split('{')
    requestInfo = rh.RequestInfo()
    requestInfo.requestId = splittedMsg[0]
    requestInfo.request = splittedMsg[1].replace('}','')
    return requestInfo