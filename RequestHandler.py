from enum import Enum
import Managers as M
import Database as db

class Request(Enum):
    LOGIN = 101
    SIGNUP = 102
    ADD = 103
    UPDATE = 104
    REMOVE = 105
    GETPASSWORDS = 106
    LOGOUT = 107
    ERROR = 300

class Response(Enum):
    LOGIN = 201
    SIGNUP = 202
    ADD = 203
    UPDATE = 204
    REMOVE = 205
    GETPASSWORDS = 206
    ERROR = 500

class RequestInfo():
    def __init__(self, requestId, request) -> None:
        self.requestId = requestId
        self.request = request

class RequestResult():
    def __init__(self, requestId, response, newHandler) -> None:
        self.requestId = requestId
        self.response = response
        self.newHandler = newHandler

class IRequestHandler():
    def isRequestRelevant(self, requestInfo) -> bool:
        pass

    def handlerRequest(self, requestInfo) -> RequestResult:
        pass


class LoginRequestHandler(IRequestHandler):
    def __init__(self) -> None:
        self.__db = db.Database()

    def isRequestRelevant(self, requestInfo) -> bool:
        return requestInfo.requestId == Request.LOGIN or requestInfo.requestId == Request.SIGNUP

    def handleRequest(self, requestInfo) -> RequestResult:
        if(requestInfo.requestId == Request.LOGIN):
            return self.login()
        elif(requestInfo.requestId == Request.SIGNUP):
            return self.signup()
        else:
            pass
    
    def login(self, requestInfo) -> RequestResult:
        info = requestInfo.request.split(',')
        if self.__db.doesUserExist(info[0]) and self.__db.doesPasswordMatch(info[0], info[1]):
            return RequestResult(Response.LOGIN.value, PasswordRequestHandler(info[0]))
        else:
            return RequestResult(Response.ERROR.value, None)

    def signup(self, requestInfo) -> RequestResult:
        info = requestInfo.request.split(',')
        if not self.__db.doesUserExist(info[0]):
            self.__db.addUser(info[0],info[1], info[2])
            return RequestResult(Response.LOGIN.value, PasswordRequestHandler(info[0]))
        else:
            return RequestResult(Response.ERROR.value, None)


class PasswordRequestHandler(IRequestHandler):
    def __init__(self, currUser) -> None:
        self.__user = currUser
        self.__db = db.Database()
    
    def isRequestRelevant(self, requestInfo) -> bool:
        return requestInfo.requestId == Request.UPDATE.value or requestInfo.requestId == Request.ADD.value or requestInfo.requestId == Request.REMOVE.value or requestInfo.requestId == Request.GETPASSWORDS.value

    def handleRequest(self, requestInfo) -> RequestResult:
        if requestInfo.requestId == Request.ADD.value:
            return self.addPassword(requestInfo)
        elif requestInfo.requestId == Request.UPDATE.value:
            return self.updatePassword(requestInfo)
        elif requestInfo.requestId == Request.REMOVE.value:
            return self.removePassword(requestInfo)
        elif requestInfo.requestId == Request.GETPASSWORDS.value:
            return self.getAllPasswords()
        else:
            pass

    def getAllPasswords(self) -> RequestResult:
        passwordsLst = self.__db.getPasswords(self.__user)
        return self.convertToRequestResult(self, Response.GETPASSWORDS.value, passwordsLst)

    def addPassword(self, requestInfo) -> RequestResult:
        info = requestInfo.request.split(',')
        passwordsLst = self.__db.addPassword(self.__user, info[0])
        return self.convertToRequestResult(self, Response.ADD.value, passwordsLst)

    def updatePassword(self, requestInfo) -> RequestResult:
        info = requestInfo.request.split(',')
        passwordsLst = self.__db.updatePassword(self.__user, info[0], info[1])
        return self.convertToRequestResult(self, Response.UPDATE.value, passwordsLst)

    def removePassword(self, requestInfo) -> RequestResult:
        info = requestInfo.request.split(',')
        passwordsLst = self.__db.deletePassword(self.__user, info[0])
        return self.convertToRequestResult(self, Response.REMOVE.value, passwordsLst)
    
    def convertToRequestResult(self, requestId, data) -> RequestResult:
        requestRes = RequestResult()
        requestRes.requestId = requestId
        requestRes.response = ','.join(data)
        requestRes.newHandler = PasswordRequestHandler(self.__user)
        return requestRes