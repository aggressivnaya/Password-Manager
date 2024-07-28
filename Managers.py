class LoginManager():
    def __init__(self) -> None:
        self.__loggedUsers = []
        #self.__db =w
    
    def signup(self, username, email):
        pass

    def login(self, username):
        pass

class PasswordManager():
    def __init__(self, currUser) -> None:
        self.__currUser = currUser
        self.__passwords = self.getAllPasswords(self, self.__currUser)
        #self.__db =
    
    def getAllPasswords(self, currUser) -> list:
        pass

    def addPassword(self, password) -> None:
        pass

    def updatePassword(self, password, newPassword) -> None:
        pass

    def removePassword(self, password) -> None:
        pass