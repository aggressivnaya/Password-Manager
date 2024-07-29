import Database as db

class LoginManager():
    def __init__(self) -> None:
        self.__db = db.Database()
        self.__loggedUsers = []
    
    def signup(self, username, email) -> None:
        pass

    def login(self, username) -> None:
        pass

    def getAllUsers(self) -> list:
        pass

class PasswordManager():
    def __init__(self, currUser) -> None:
        self.__db = db.Database()
        self.__currUser = currUser
        self.__passwords = self.getAllPasswords(self, self.__currUser)
    
    def getAllPasswords(self, currUser) -> list:
        pass

    def addPassword(self, password) -> None:
        pass

    def updatePassword(self, password, newPassword) -> None:
        pass

    def removePassword(self, password) -> None:
        pass