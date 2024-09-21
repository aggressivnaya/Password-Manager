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
                versionId INTEGER NOT NULL,
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
        
        self.__cursor.execute('''
            CREATE TABLE IF NOT EXISTS requests(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                userId TEXT NOT NULL,
                requestCommand TEXT NOT NULL,
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
            passwordId = self.__cursor.fetchall() 
            if passwordId:
                return list(passwordId)  # Return the password id
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
                #decodedPasswords = []
                #for i in passwords:
                 #   decodedPasswords.append(str(e.decryption(i)))
                return passwords
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


    def addPassword(self, username, name, password, isShared):
        try:
            #encryptedPassword = e.encryption(password)
            self.__cursor.execute('''
                INSERT INTO passwords (name, password, shared) VALUES (?, ?, ?)''', 
                (name, password, isShared)
            )
            self.__conn.commit()
            print(f"Password {name} added successfully.")
            userId = self.findUserIdByUsername(username)
            passwordId = self.findPasswordIdByPassword(password)
            self.assignPasswordToUser(userId, passwordId)
            self.addHistoryEntry(userId, passwordId, "ADD")
            return True
        except Exception as e:
            print(f"An error occurred while adding password: {e}")
            return False


    def updatePassword(self, username, passwordId, newName, newPassword, isShared):
        try:
            #newEncryptedPassword = e.encryption(newPassword)
            self.__cursor.execute('''
                UPDATE passwords SET name = ?, password = ?, shared = ? WHERE id = ?''', 
                (newName, newPassword, isShared, passwordId)
            )
            self.__conn.commit()
            print(f"Password with ID {passwordId} updated successfully.")
            userId = self.findUserIdByUsername(username)
            self.addHistoryEntry(userId, passwordId, "UPDATE")
            return True
        except Exception as e:
            print(f"An error occurred while updating password: {e}")
            return False

    def deletePassword(self, username, passwordId):
        try:
            self.__cursor.execute('''
                DELETE FROM passwords WHERE id = ?''', 
                (passwordId,)
            )
            self.__conn.commit()
            print(f"Password with ID {passwordId} deleted successfully.")
            userId = self.findUserIdByUsername(username)
            self.__cursor.execute('''
                DELETE FROM usersPasswords WHERE userId = ? AND passwordId = ?''', 
                (userId, passwordId,)
            )
            self.__conn.commit()

            self.addHistoryEntry(userId, passwordId, "DELETE")
            return True
        except Exception as e:
            print(f"An error occurred while deleting password: {e}")
            return False

    def addHistoryEntry(self, userId, passwordId, method):
        try:
            date = datetime.datetime.now()
            versionId = self.getLastVersionOfPassword(passwordId)
            if not versionId == None:
                versionId += 1
            else:
                versionId = 1
            
            self.__cursor.execute('''
                INSERT INTO history (versionId, passwordId, method, date)
                VALUES(?, ?, ?, ?)''', 
                (versionId, passwordId, method, date)
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
                return int(versionId[0])  # Returns the latest method and date for the password
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
            return True
        except Exception as e:
            print(f"Error assigning password user: {e}")
            return False

    def getHistoryOfUser(self, userId, passwordId=0):
        passwordsIds = self.findPasswordIdByUserId(userId)
        historyOfAllPasswords = []
        try:
            for password in passwordsIds:
                self.__cursor.execute('''
                    SELECT * FROM history WHERE passwordId = ? ORDER BY date DESC
                    LIMIT 5
                    ''', (password,))
                result = list(self.__cursor.fetchall())
                if result:
                    for i in result:
                        historyOfAllPasswords.append(i)
                else:
                    return None
            return historyOfAllPasswords
        except Exception as e:
            print(f"Error getting the history of the user: {e}")
            return None

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

    def createGroup(self, adminId, name, description):
        try:
            self.__cursor.execute('''
                INSERT INTO groups (name, description) VALUES(?, ?)
                ''', (name, description))
            self.__conn.commit()
            groupId = self.__cursor.lastrowid
            print(groupId)
            #groupId = self.getGroupIdByUserId(adminId, True)
            self.enterGroup(adminId, groupId, True)

            return True
        except Exception as e:
            print(f"Error creating group: {e}")
            return False

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

    def deleteRequest(self, adminId, groupId, command):
        try:
            self.__cursor.execute('''
                DELETE FROM request WHERE userId = ? AND gorupId = ? AND requestCommand = ?
                ''', (adminId, groupId, command))
            self.__conn.commit()
            return True
        except Exception as e:
            print(f"Error delete request: {e}")
            return False

    def checkAdmin(self, groupId, userId):
        try:
            self.__cursor.execute('''
                SELECT isAdmin FROM usersGroups WHERE groupId = ? AND userId = ?
                ''', (groupId, userId,))
            
            isAdmin = self.__cursor.fetchone()[0]
            if isAdmin == "True":
                return True
            else:
                return False
        except Exception as e:
            print(f"Error checking the admin: {e}")
            return False

    def acceptToGroup(self, adminId, userId, groupId):
        if self.checkAdmin(groupId, adminId):
            self.enterGroup(userId, groupId)
            return True
        else:
            return False

    def enterGroup(self, userId, groupId, isAdmin=False):
        try:
            self.__cursor.execute('''
                INSERT INTO usersGroups(userId, isAdmin, groupId) VALUES(?, ?, ?)
                ''',(userId, isAdmin, groupId))
            self.__conn.commit()
            return True
        except Exception as e:
            print(f"Error with entering the group: {e}")
            return False
    
    def leaveGroup(self, userId, groupId):
        try:
            self.__cursor.execute('''
                DELETE FROM usersGroups WHERE userId = ? AND groupId = ?
                ''', (userId, groupId))
            self.__conn.commit()
            return True
        except Exception as e:
            print(f"Error with leaving the group: {e}")
            return False

    def removeFromGroup(self, adminId, userId, groupId):
        '''
        In the my server only the admin of the group can remove other users, so we need to check is the userId is the admin
        '''
        try:
            if not self.checkAdmin(groupId, adminId):
                raise Exception("invalid admin id")
            self.leaveGroup(userId, groupId)

            return True
        except Exception as e:
            print(f"Error with remove user from group: {e}")
            return False

    def removeGroup(self, adminId, groupId):
        '''
        In the my server only the admin of the group can remove the group, so we need to check is the userId is the admin
        '''
        try:
            if not self.checkAdmin(adminId):
                raise Exception("invalid admin id")
            self.__cursor.execute('''
                DELETE FROM groups WHERE id = ?
                ''',(groupId))
            
            self.__cursor.execute('''
                DELETE FROM usersGroups WHERE groupId = ?
                ''', (groupId))
            
            self.__conn.commit()
            return True
        except Exception as e:
            print(f"Error with removing the group: {e}")
            return False

    def getSharedPasswords(self, groupId):
        try:
            self.__cursor.execute('''
                SELECT p.id, p.name, p.password, p.shared
                FROM passwords p
                JOIN usersPasswords up ON p.id = up.passwordId
                JOIN usersGroups ug ON up.userId = ug.userId
                WHERE ug.groupId = ?
                AND p.shared = 'True'
                ''',(groupId,))
            
            requests = self.__cursor.fetchall()
            return requests
        except Exception as e:
            print(f"Error with getting shared passwords: {e}")
            return False
        
    def getGroupInfo(self, groupId):
        try:
            self.__cursor.execute('''
                SELECT * FROM groups WHERE id = ?
                ''', (groupId,))
            
            requests = self.__cursor.fetchall()

            groupMetadata = [
                {
                    'id': row[0],
                    'name': row[1],
                    'description': row[2]
                }
                for row in requests
            ]
            return groupMetadata
        except Exception as e:
            print(f"Error with getting the info of the group: {e}")
            return False

    def logoutFromServer(self, userId):
        try:
            passwords = self.getPasswordsForUser(userId)
            if len(passwords) >= 1:
                for password in passwords:
                    passID = password[0]
                    print(passID)
                    self.deletePassword(userId, passID)

                self.__cursor.execute('''
                    DELETE FROM usersPasswords WHERE userId = ?
                    ''', (userId,))
                self.__conn.commit()


            self.__cursor.execute('''
                DELETE FROM usersGroups WHERE userId = ?
                ''', (userId))
            self.__conn.commit()

            print("deleting other stuff")
            self.__cursor.execute('''
                DELETE FROM users WHERE id = ?
                ''', (userId,))
            self.__conn.commit()            
            
        except Exception as e:
            print(f"Error with logout: {e}")
            return False