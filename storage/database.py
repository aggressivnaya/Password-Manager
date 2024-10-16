import sqlite3
import enum as Enum
import EncryptionDecryption as e
from IDatabase import IDatabase

class Database(IDatabase):
    def __init__(self) -> None:
        self.onn = sqlite3.connect('passwordMangerDB.db', check_same_thread=False)
        #self.__conn = sqlite3.connect('testing2.db')
        self.cursor = self.conn.cursor()

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                email TEXT NOT NULL
            )''') 

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS passwords (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                password TEXT NOT NULL,
                shared TEXT NOT NULL
            )''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS history(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                versionId INTEGER NOT NULL,
                passwordId INTEGER NOT NULL,
                method TEXT NOT NULL,
                date TEXT NOT NULL,
                FOREIGN KEY (passwordId) REFERENCES passwords(id)
            )''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS usersPasswords (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                userId INTEGER NOT NULL,
                passwordId INTEGER NOT NULL,
                FOREIGN KEY (userId) REFERENCES users(id),
                FOREIGN KEY (passwordId) REFERENCES passwords(id)
            )''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS groups (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT NOT NULL
            )''') 
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS usersGroups (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                userId TEXT NOT NULL,
                isAdmin TEXT NOT NULL,
                groupId TEXT NOT NULL,
                FOREIGN KEY (userId) REFERENCES users(id),
                FOREIGN KEY (groupId) REFERENCES groups(id)
            )''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS requests(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                userId TEXT NOT NULL,
                requestCommand TEXT NOT NULL,
                groupId TEXT NOT NULL,
                FOREIGN KEY (userId) REFERENCES users(id),
                FOREIGN KEY (groupId) REFERENCES groups(id)
            )''')
        
        self.conn.commit()

    #added to user
    #def findUserIdByUsername(self, username):
    
    #added to password 
    #def findPasswordIdByPassword(self, password):

    #added to password 
    #def findPasswordById(self, passwordId):

    #added to password  
    #def findPasswordIdByUserId(self, userId):

    #added to user
    #def doesUserExist(self, username) -> bool:

    '''def doesPasswordMatch(self, username, enteredPass) -> bool:
        self.__cursor.execute(
        SELECT password FROM users
        WHERE username = ? AND password = ? ,(username, enteredPass,))
        rows = self.__cursor.fetchall()
        passwords = [row[0] for row in rows]

        return len(passwords) > 0'''

    '''def getUsers(self) -> list:
        self.__cursor.execute('SELECT username FROM users')
        rows = self.__cursor.fetchall()
        users = [row[0] for row in rows]

        return users'''

    #added to password
    #def getPasswordsForUser(self, userId):

    #added to user
    #def addUser(self, username, email):
    
    #added to password
    #def addPassword(self, username, name, password, isShared):
    
    #added to password
    #def updatePassword(self, username, passwordId, newName, newPassword, isShared):
     
    #added to password
    #def deletePassword(self, username, passwordId):

    #added to password
    #def addHistoryEntry(self, userId, passwordId, method):
    
    #added to password
    #def getLastVersionOfPassword(self, passwordId):

    #added to password
    #def getPasswordNameById(self, passwordId):

    #added to password
    #def assignPasswordToUser(self, userId, passwordId):

    #added to user
    #def getHistoryOfUser(self, userId, passwordId=0):

    '''def getGroupIdByUserId(self, userId):
        try:
            #last group means that is the last group that added to the database
          
                #getting all the group that user has
                self.__cursor.execute(
                    SELECT groupId
                    FROM usersGroups
                    WHERE userId = ?
                , (userId,))
                
                groupsIds = list(self.__cursor.fetchall())
                return groupsIds
        except Exception as e:
            print(f"Error getting group id: {e}")
            return False'''

    #def createGroup(self, adminId, name, description):

    def listOfRequests(self, adminId, groupId):
        try:
            self.__cursor.execute('''
                SELECT * FROM requests WHERE userId = ? AND groupId = ?
                ''',(adminId, groupId,))
            
            requests = self.__cursor.fetchall()
            return list(requests)
        except Exception as e:
            print(f"Error getting list of requests of group: {e}")
            return False
        
    def addRequest(self, userId, groupId ,command):
        try:
            self.__cursor.execute('''
                INSERT INTO requests(userId, requestCommand, groupId) VALUES(?, ?, ?)
                ''', (userId, command, groupId))
            self.__conn.commit()
            return True
        except Exception as e:
            print(f"Error insert request; {e}")
            return False

    def deleteRequest(self, adminId, groupId, command):
        try:
            self.__cursor.execute('''
                DELETE FROM requests WHERE userId = ? AND gorupId = ? AND requestCommand = ?
                ''', (adminId, groupId, command,))
            self.__conn.commit()
            return True
        except Exception as e:
            print(f"Error delete request: {e}")
            return False

    #added to group
    #def checkAdmin(self, groupId, userId):

    #def acceptToGroup(self, adminId, userId, groupId):

    #def enterGroup(self, userId, groupId, isAdmin=False):
    
    #def leaveGroup(self, userId, groupId):

    #def removeFromGroup(self, adminId, userId, groupId):

    #def removeGroup(self, adminId, groupId):

    #added to password
    #def getSharedPasswords(self, groupId):
        
    #def getGroupInfo(self, groupId):

    #added to user
    #def logoutFromServer(self, userId):