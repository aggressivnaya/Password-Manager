import sqlite3

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
        self.__cursor.execute('''
        SELECT id FROM passwords WHERE password = ?
        ''', (password,))
        rows = self.__cursor.fetchall()
        passwordId = [row[0] for row in rows]

        return passwordId[0]

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

        return passwords

    def addUser(self, username, password, email):
        self.__cursor.execute('''
        INSERT INTO users (username, password, email)
        VALUES (?, ?, ?)
        ''', (username, password, email,))
        self.__conn.commit()

    def addPassword(self, username, password):
        self.__cursor.execute('''
        INSERT INTO passwords (password, username)
        VALUES (?, ?)
        ''', (password, username))
        self.__conn.commit()

        return self.getPasswords(username)

    def updatePassword(self, username, currPassword, newPassword):
        print("upd func in db")
        passId = self.findPasswordId(currPassword)
        self.__cursor.execute('''
        UPDATE passwords
        SET password = ?
        WHERE id = ?
        ''', (newPassword, passId,))
        self.__conn.commit()

        return self.getPasswords(username)

    def deletePassword(self, username, password):
        print("del func in db")
        self.__cursor.execute('''
        DELETE FROM passwords
        WHERE password = ? AND username = ?
        ''',(password, username,))
        self.__conn.commit()

        return self.getPasswords(username)