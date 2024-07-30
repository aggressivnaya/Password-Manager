import socket
import select
import RequestHandler as rh

LISTEN_PORT = 90
class Server:
    def __init__(self) -> None:
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
                            self.__sockets[client_soc] = rh.LoginRequestHandler()
                        else:
                            # Handle data from the connected clients
                            msg = s.recv(1024).decode()
                            print(f"Received data: {msg} from {s.getpeername()}")
                            if msg:
                                requestInfo = convertRecievedMsg(msg)
                                if requestInfo.requestId == rh.Request.LOGOUT:
                                    print(f"Closing connection to {s.getpeername()}")
                                    self.__sockets.remove(s)
                                    s.close()

                                handler = self.__sockets[client_soc]
                                if handler.isRequestRelevant(requestInfo.requestId):
                                    requestResult = handler.handlerRequest(requestInfo)
                                    if requestResult.newHandler == None:
                                        raise Exception("new handler is none")
                                    
                                    s.sendall(requestResult.response.encode())
                                    self.__sockets[client_soc] = requestResult.newHandler
                            else:
                                # If no data is received, the client has closed the connection
                                print(f"Closing connection to {s.getpeername()}")
                                self.__sockets.remove(s)
                                s.close()
        except Exception as e:
            print(e)


def convertRecievedMsg(msg) -> rh.RequestInfo:
    splittedMsg =  msg.split('[')
    requestInfo = rh.RequestInfo()
    requestInfo.requestId = splittedMsg[0]
    requestInfo.request = splittedMsg[1].replace(']','')
    return requestInfo

def main():
    server = Server()
    server.run()

if __name__ == "__main__":
    main()