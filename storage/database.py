import sqlite3
import enum as Enum
import EncryptionDecryption as e

class Database():
    def __init__(self) -> None:
        #self.__conn = sqlite3.connect('passwordMangerDB.db')
        self.__conn = sqlite3.connect('testing2.db')
        self.__cursor = self.__conn.cursor()

        self.__cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                password TEXT NOT NULL,
                email TEXT NOT NULL
            )''') 

        self.__cursor.execute('''
            CREATE TABLE IF NOT EXISTS passwords (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                password TEXT NOT NULL,
                username TEXT NOT NULL 
            )''')

        self.__conn.commit()

    def findPasswordId(self, password) -> int :
        encryptedPassword = e.encryption(password)
        self.__cursor.execute('''
        SELECT id FROM passwords WHERE password = ?
        ''', (encryptedPassword,))
        rows = self.__cursor.fetchall()
        passwordId = [row[0] for row in rows]

        return passwordId[0]
    
    def findPasswordById(self, passwordId) -> int :
        self.__cursor.execute('''
        SELECT id FROM passwords WHERE id = ?
        ''', (passwordId,))
        rows = self.__cursor.fetchall()
        password = [row[0] for row in rows]

        return str(e.decryption(password[0]))

    def doesUserExist(self, username) -> bool:
        self.__cursor.execute('''
        SELECT username FROM users
        WHERE username = ?''', (username,))
        rows = self.__cursor.fetchall()
        users = [row[0] for row in rows]

        return len(users) > 0

    def doesPasswordMatch(self, username, enteredPass) -> bool:
        self.__cursor.execute('''
        SELECT password FROM users
        WHERE username = ? AND password = ? ''',(username, enteredPass,))
        rows = self.__cursor.fetchall()
        passwords = [row[0] for row in rows]

        return len(passwords) > 0

    def getUsers(self) -> list:
        self.__cursor.execute('SELECT username FROM users')
        rows = self.__cursor.fetchall()
        users = [row[0] for row in rows]

        return users

    def getPasswords(self, username) -> list:
        self.__cursor.execute('''SELECT password FROM passwords WHERE username = ? ''',(username,))
        rows = self.__cursor.fetchall()
        passwords = [row[0] for row in rows]
        decodedPasswords = []
        for i in passwords:
            decodedPasswords.append(str(e.decryption(i)))

        return decodedPasswords

    def addUser(self, username, password, email):
        self.__cursor.execute('''
        INSERT INTO users (username, password, email)
        VALUES (?, ?, ?)
        ''', (username, password, email,))
        self.__conn.commit()

    def addPassword(self, username, password):
        encryptedPassword = e.encryption(password)
        self.__cursor.execute('''
        INSERT INTO passwords (password, username)
        VALUES (?, ?)
        ''', (encryptedPassword, username))
        self.__conn.commit()
        
        return self.getPasswords(username)

    def updatePassword(self, username, currPasswordID, newPassword):
        newEncryptedPassword = e.encryption(newPassword)
        self.__cursor.execute('''
        UPDATE passwords
        SET password = ?
        WHERE id = ?
        ''', (newEncryptedPassword, currPasswordID,))
        self.__conn.commit()

        return self.getPasswords(username)

    def deletePassword(self, username, password):
        encryptedPassword = e.encryption(password)
        self.__cursor.execute('''
        DELETE FROM passwords
        WHERE password = ? AND username = ?
        ''',(encryptedPassword, username,))
        self.__conn.commit()

        return self.getPasswords(username)