from enum import Enum
import Managers as M

class Request(Enum):
    LOGIN = 101
    SIGNUP = 102
    ADD = 103
    UPDATE = 104
    REMOVE = 105
    LOGOUT = 106
    ERROR = 300

class Response(Enum):
    LOGIN = 201
    SIGNUP = 202
    ADD = 203
    UPDATE = 204
    REMOVE = 205

class RequestInfo():
    def __init__(self, requestId, request) -> None:
        self.requestId = requestId
        self.request = request

class RequestResult():
    def __init__(self, response, newHandler) -> None:
        self.response = response
        self.newHandler = newHandler

class IRequestHandler():
    def isRequestRelevant(self, requestInfo) -> bool:
        pass

    def handlerRequest(self, requestInfo) -> RequestResult:
        pass

class LoginRequestHandler(IRequestHandler):
    def __init__(self, currUser) -> None:
        self.__user = currUser
        self.__loginManager = M.LoginManager()

    def isRequestRelevant(self, requestInfo) -> bool:
        return requestInfo.requestId ==Request.LOGIN or requestInfo.requestId == Request.SIGNUP

    def handleRequest(self, requestInfo) -> RequestResult:
        if(requestInfo.requestId == Request.LOGIN):
            return self.login()
        elif(requestInfo.requestId == Request.SIGNUP):
            return self.signup()
        else:
            pass
    
    def login(self, requestInfo) -> RequestResult:
        pass

    def signup(self, requestInfo) -> RequestResult:
        pass

    def setUser(self, user) -> None:
        self.__user = user

    #def logout(requestInfo) -> RequestResult:
     #   pass
    
class PasswordRequestHandler(IRequestHandler):
    def __init__(self, currUser) -> None:
        self.__user = currUser
        self.__passwordManager = M.PasswordManager()
    
    def isRequestRelevant(self, requestInfo) -> bool:
        return requestInfo.requestId ==Request.UPDATE or requestInfo.requestId == Request.ADD or requestInfo.requestId == Request.REMOVE

    def handleRequest(self, requestInfo) -> RequestResult:
        if(requestInfo.requestId == Request.ADD):
            return self.__passwordManager.addPassword(requestInfo.request)
        elif(requestInfo.requestId == Request.UPDATE):
            return self.__passwordManager.updatePassword(requestInfo.request)
        elif(requestInfo.requestId == Request.REMOVE):
            return self.__passwordManager.removePassword(requestInfo.request)
        else:
            pass

    def getAllPasswords(self, requestInfo) -> RequestResult:
        pass