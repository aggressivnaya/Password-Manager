from enum import Enum

class RHerrors(Enum):
    LOGIN = 'error of login'
    SIGNUP = 'error of signup'

class RHexception(Enum):
    ELOGINHANDLER = 'something went wrong in login handler'
    EPASSWORDHANDLER = 'something went wrong in password handler'

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
    LOGOUT = 207
    ERROR = 500

class RequestInfo():
    '''
    msg that we getting from client
    requestId : msg type
    requst : components of the msg
    '''
    def __init__(self, requestId, request) -> None:
        self.requestId = int(requestId)
        self.request = request

class RequestResult():
    '''
    msg that we are sending to client
    requestId : msg type
    response : msg from the server
    newHandler : the next handler
    '''
    def __init__(self, requestId, response, newHandler) -> None:
        self.requestId = requestId 
        self.response = response
        self.newHandler = newHandler

class IRequestHandler():
    def isRequestRelevant(self, requestInfo) -> bool:
        pass

    def handlerRequest(self, requestInfo) -> RequestResult:
        pass

    def logoutRequest(self) -> RequestResult:
        return RequestResult(Response.LOGOUT.value, "", None)


class LoginRequestHandler(IRequestHandler):
    '''
    this class is managing all the func that bind with login
    '''
    def __init__(self, db) -> None:
        self.__db = db

    def isRequestRelevant(self, requestId) -> bool:
        return requestId == Request.LOGIN.value or requestId == Request.SIGNUP.value or requestId == Request.LOGOUT.value

    def handleRequest(self, requestInfo) -> RequestResult:
        if requestInfo.requestId == Request.LOGIN.value:
            return self.login(requestInfo)
        elif requestInfo.requestId == Request.SIGNUP.value:
            return self.signup(requestInfo)
        elif requestInfo.requestId == Request.LOGOUT.value:
            return IRequestHandler.logoutRequest(self)
        else:
            raise Exception(RHexception.ELOGINHANDLER.value)
    
    def login(self, requestInfo) -> RequestResult:
        info = requestInfo.request.split(',')
        if self.__db.doesUserExist(info[0]) and self.__db.doesPasswordMatch(info[0], info[1]):
            return RequestResult(Response.LOGIN.value, "",PasswordRequestHandler(info[0], self.__db))
        else:
            return RequestResult(Response.ERROR.value, RHerrors.LOGIN.value ,None)

    def signup(self, requestInfo) -> RequestResult:
        info = requestInfo.request.split(',')
        print(self.__db.doesUserExist(info[0]))
        if self.__db.doesUserExist(info[0]) == False:
            self.__db.addUser(info[0],info[1], info[2])
            return RequestResult(Response.SIGNUP.value, "", PasswordRequestHandler(info[0], self.__db))
        else:
            return RequestResult(Response.ERROR.value, RHerrors.SIGNUP.value ,None)


class PasswordRequestHandler(IRequestHandler):
    '''
    this class is managing all the func that bind with passwords
    '''
    def __init__(self, currUser, db) -> None:
        self.__user = currUser
        self.__db = db
    
    def isRequestRelevant(self, requestId) -> bool:
        return requestId == Request.UPDATE.value or requestId == Request.ADD.value or requestId == Request.REMOVE.value or requestId == Request.GETPASSWORDS.value or requestId == Request.LOGOUT.value

    def handleRequest(self, requestInfo) -> RequestResult:
        if requestInfo.requestId == Request.ADD.value:
            return self.addPassword(requestInfo)
        elif requestInfo.requestId == Request.UPDATE.value:
            return self.updatePassword(requestInfo)
        elif requestInfo.requestId == Request.REMOVE.value:
            return self.removePassword(requestInfo)
        elif requestInfo.requestId == Request.GETPASSWORDS.value:
            return self.getAllPasswords()
        elif requestInfo.requestId == Request.LOGOUT.value:
            return IRequestHandler.logoutRequest(self)
        else:
            raise Exception(RHexception.EPASSWORDHANDLER.value)

    def getAllPasswords(self) -> RequestResult:
        passwordsLst = self.__db.getPasswords(self.__user)
        return self.convertToRequestResult(Response.GETPASSWORDS.value, passwordsLst)

    def addPassword(self, requestInfo) -> RequestResult:
        info = requestInfo.request.split(',')
        passwordsLst = self.__db.addPassword(self.__user, info[0])
        return self.convertToRequestResult(Response.ADD.value, passwordsLst)

    def updatePassword(self, requestInfo) -> RequestResult:
        info = requestInfo.request.split(',')
        passwordsLst = self.__db.updatePassword(self.__user, info[0], info[1])
        return self.convertToRequestResult(Response.UPDATE.value, passwordsLst)

    def removePassword(self, requestInfo) -> RequestResult:
        info = requestInfo.request.split(',')
        passwordsLst = self.__db.deletePassword(self.__user, info[0])
        return self.convertToRequestResult(Response.REMOVE.value, passwordsLst)
    
    def convertToRequestResult(self, requestId, data) -> RequestResult:
        print(data)
        requestRes = RequestResult(requestId, ','.join(data), PasswordRequestHandler(self.__user, self.__db))
        return requestRes