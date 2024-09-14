class IDatabase():
    def __init__(self) -> None:
        pass

    def doesUserExist(self, username) -> bool:
        pass

    def getPasswordsForUser(self, userId):
        pass

    def addUser(self, username, email):
        pass

    def addPassword(self, username, name, password):
        pass

    def updatePassword(self, username, passwordId, newName, newPassword):
        pass

    def deletePassword(self, username, passwordId):
        pass

    def addHistoryEntry(self, userId, passwordId, method):
        pass

    def assignPasswordToUser(self, userId, passwordId):
        pass

    def getHistoryOfUser(self, userId):
        pass