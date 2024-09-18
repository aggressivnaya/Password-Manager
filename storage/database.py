import sqlite3
import enum as Enum
import EncryptionDecryption as e
import datetime
from IDatabase import IDatabase

class Database(IDatabase):
    def __init__(self) -> None:
        self.__conn = sqlite3.connect('passwordMangerDB.db', check_same_thread=False)
        #self.__conn = sqlite3.connect('testing2.db')
        self.__cursor = self.__conn.cursor()

        self.__cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                email TEXT NOT NULL
            )''') 

        self.__cursor.execute('''
            CREATE TABLE IF NOT EXISTS passwords (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                password TEXT NOT NULL,
                shared TEXT NOT NULL
            )''')
        
        self.__cursor.execute('''
            CREATE TABLE IF NOT EXISTS history(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                passwordId INTEGER NOT NULL,
                method TEXT NOT NULL,
                date TEXT NOT NULL,
                FOREIGN KEY (passwordId) REFERENCES passwords(id)
            )''')
        
        self.__cursor.execute('''
            CREATE TABLE IF NOT EXISTS usersPasswords (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                userId INTEGER NOT NULL,
                passwordId INTEGER NOT NULL,
                FOREIGN KEY (userId) REFERENCES users(id),
                FOREIGN KEY (passwordId) REFERENCES passwords(id)
            )''')
        
        self.__cursor.execute('''
            CREATE TABLE IF NOT EXISTS groups (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT NOT NULL
            )''') 
        
        self.__cursor.execute('''
            CREATE TABLE IF NOT EXISTS usersGroups (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                userId TEXT NOT NULL,
                isAdmin TEXT NOT NULL,
                groupId TEXT NOT NULL,
                FOREIGN KEY (userId) REFERENCES users(id),
                FOREIGN KEY (groupId) REFERENCES groups(id)
            )''') 
        
        self.__conn.commit()

    def findUserIdByUsername(self, username):
        try:
            self.__cursor.execute('''
                SELECT id FROM users WHERE username = ?''', (username,)
            )
            userId = self.__cursor.fetchone()
            if userId:
                return userId[0]
            else:
                return None
        except Exception as e:
            print(f"An error occurred while finding user ID by username: {e}")
            return None
        
    def findPasswordIdByPassword(self, password):
        try:
            self.__cursor.execute('''
                SELECT id FROM passwords WHERE password = ?''', (password,)
            )
            passwordId = self.__cursor.fetchone()
            if passwordId:
                return passwordId[0]
            else:
                return None
        except Exception as e:
            print(f"An error occurred while finding password ID by password: {e}")
            return None
        
    def findPasswordById(self, passwordId):
        try:
            self.__cursor.execute('''
                SELECT password FROM passwords WHERE id = ?''', (passwordId,)
            )
            password = self.__cursor.fetchone() 
            if password:
                return password[0]  # Return the encrypted password
            else:
                return None 
        except Exception as e:
            print(f"An error occurred while finding user ID by username: {e}")
            return None
        
    def findPasswordIdByUserId(self, userId):
        try:
            self.__cursor.execute('''
                SELECT passwordId FROM usersPasswords WHERE userId = ?''', (userId,)
            )
            passwordId = self.__cursor.fetchone() 
            if passwordId:
                return passwordId[0]  # Return the password id
            else:
                return None 
        except Exception as e:
            print(f"An error occurred while finding user ID by username: {e}")
            return None

    def doesUserExist(self, username) -> bool:
        self.__cursor.execute('''
        SELECT id FROM users
        WHERE username = ?''', (username,))
        users = self.__cursor.fetchall()

        return len(users) > 0

    def doesPasswordMatch(self, username, enteredPass) -> bool:
        self.__cursor.execute('''
        SELECT password FROM users
        WHERE username = ? AND password = ? ''',(username, enteredPass,))
        rows = self.__cursor.fetchall()
        passwords = [row[0] for row in rows]

        return len(passwords) > 0

    '''def getUsers(self) -> list:
        self.__cursor.execute('SELECT username FROM users')
        rows = self.__cursor.fetchall()
        users = [row[0] for row in rows]

        return users'''

    def getPasswordsForUser(self, userId):
        try:
            self.__cursor.execute('''
                SELECT p.id, p.name, p.password FROM passwords p
                JOIN usersPasswords up ON p.id = up.passwordId
                WHERE up.userId = ?''', 
                (userId,)
            )
            passwords = self.__cursor.fetchall()
            if passwords:
                decodedPasswords = []
                for i in passwords:
                    decodedPasswords.append(str(e.decryption(i)))
                return decodedPasswords
            else:
                return []
        except Exception as e:
            print(f"An error occurred while fetching passwords for user: {e}")
            return []

    def addUser(self, username, email):
        try:
            self.__cursor.execute('''
                INSERT INTO users (username, email) VALUES (?, ?)''', 
                (username, email)
            )
            self.__conn.commit()
            print(f"User {username} added successfully.")
        except Exception as e:
            print(f"An error occurred while adding user: {e}")


    def addPassword(self, username, name, password):
        try:
            encryptedPassword = e.encryption(password)
            self.__cursor.execute('''
                INSERT INTO passwords (name, password) VALUES (?, ?)''', 
                (name, encryptedPassword)
            )
            self.__conn.commit()
            print(f"Password {name} added successfully.")
            userId = self.findUserIdByUsername(username)
            passwordId = self.findPasswordIdByPassword(password)
            self.assignPasswordToUser(userId, passwordId)
            self.addHistoryEntry(userId, passwordId, "ADD")
        except Exception as e:
            print(f"An error occurred while adding password: {e}")


    def updatePassword(self, username, passwordId, newName, newPassword):
        try:
            newEncryptedPassword = e.encryption(newPassword)
            self.__cursor.execute('''
                UPDATE passwords SET name = ?, password = ? WHERE id = ?''', 
                (newName, newEncryptedPassword, passwordId)
            )
            self.__conn.commit()
            print(f"Password with ID {passwordId} updated successfully.")
            userId = self.findUserIdByUsername(username)
            self.addHistoryEntry(userId, passwordId, "UPDATE")
        except Exception as e:
            print(f"An error occurred while updating password: {e}")

    def deletePassword(self, username, passwordId):
        try:
            self.__cursor.execute('''
                DELETE FROM passwords WHERE id = ?''', 
                (passwordId,)
            )
            self.__conn.commit()
            print(f"Password with ID {passwordId} deleted successfully.")
            userId = self.findUserIdByUsername(username)
            self.addHistoryEntry(userId, passwordId, "DELETE")
        except Exception as e:
            print(f"An error occurred while deleting password: {e}")

    def addHistoryEntry(self, userId, passwordId, method):
        try:
            date = datetime.datetime.now()
            versionId = self.getLastVersionOfPassword(passwordId) + 1
            name = self.getPasswordNameById(passwordId)
            password = self.findPasswordById(passwordId)
            self.__cursor.execute('''
                INSERT INTO history (versionId, userId, name, password, passwordId, method, date)
                VALUE(?, ?, ?, ?, ?, ?, ?)''', 
                (versionId, userId, name, password, passwordId, method, date)
            )
            self.__conn.commit()
            print(f"Added the change to history table successfully.")
        except Exception as e:
            print(f"An error occurred while adding to history: {e}")

    def getLastVersionOfPassword(self, passwordId):
        try:
            self.__cursor.execute('''
                SELECT versionId
                FROM history
                WHERE passwordId = ?
                ORDER BY versionId DESC
                LIMIT 1
            ''', (passwordId,))
            
            versionId = self.__cursor.fetchone()
            if versionId:
                return int(versionId)  # Returns the latest method and date for the password
            else:
                return None  # Returns None if no version is found
        except Exception as e:
            print(f"An error occurred while getting the latest version of password: {e}")
            return None

    def getPasswordNameById(self, passwordId):
        try:
            self.__cursor.execute('''
                SELECT name
                FROM passwords
                WHERE id = ?
            ''', (passwordId,))
            
            result = self.__cursor.fetchone()
            
            if result:
                return result[0]  # Returning the name (first column in result)
            else:
                return None  # No password found with the given ID
        
        except Exception as e:
            print(f"Error retrieving password name: {e}")
            return None

    def assignPasswordToUser(self, userId, passwordId):
        try:
            self.__cursor.execute('''
                INSERT INTO usersPasswords (userId, passwordId) 
                VALUES (?, ?)
                ''', (userId, passwordId))
            self.__conn.commit()
            print(f"Password {passwordId} assigned to user {userId} successfully.")
        except Exception as e:
            print(e)

    def getHistoryOfUser(self, userId):
        passwordId = self.findPasswordIdByUserId(userId)
        try:
            self.__cursor.execute('''
                SELECT * FROM history WHERE passwordId = ?
                ''', (passwordId,))
            
            result = self.__cursor.fetchone()
            
            if result:
                return result
            else:
                return None 
        
        except Exception as e:
            print(e)

    def createGroup(self, adminId, name, description):
        pass

    def listOfRequestsToEnter(self, adminId, groupId):
        pass

    def acceptToGroup(self, adminId, userId, groupId):
        pass

    def enterGroup(self, userId, groupId):
        pass
    
    def leaveGroup(self, userId, groupId):
        pass

    def removeFromGroup(self, adminId, userId, groupId):
        pass

    def removeGroup(self, adminId, groupId):
        pass

    def getSharedPasswords(self, groupId):
        pass

    def logoutFromServer(self, userId):
        pass