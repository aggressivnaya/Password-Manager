import sqlite3

class Database():
    def __init__(self) -> None:
        self.__conn = sqlite3.connect('passwordMangerDB.db')
        self.__cursor = self.__conn.cursor()
        self.__cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            email TEXT NOT NULL,
            PRIMARY KEY (username)
        )''')

        self.__cursor.execute('''
        CREATE TABLE IF NOT EXISTS passwords (
            password TEXT NOT NULL,
            username TEXT NOT NULL,
            PRIMARY KEY (username),
            FOREIGN KEY (username) REFERENCES users(username)
        )''')

        self.__conn.commit()

    def doesUserExist(self, username) -> bool:
        self.__cursor.execute('''
        SELECT username FROM users
        WHERE username = ? ''',(username))
        rows = self.__cursor.fetchall()
        users = [row[0] for row in rows]

        return len(users) > 0

    def doesPasswordMatch(self, username, enteredPass) -> bool:
        self.__cursor.execute('''
        SELECT password FROM users
        WHERE username = ? AND password = ? ''',(username, enteredPass))
        rows = self.__cursor.fetchall()
        passwords = [row[1] for row in rows]

        return len(passwords) > 0

    def getUsers(self) -> list:
        self.__cursor.execute('SELECT username FROM users')
        rows = self.__cursor.fetchall()

        # Extract users into a list of strings
        users = [row[0] for row in rows]
        return users

    def getPasswords(self, username) -> list:
        self.__cursor.execute('SELECT password FROM passwords WHERE username = ? ',(username))
        rows = self.__cursor.fetchall()

        # Extract passwords into a list of strings
        passwords = [row[0] for row in rows]
        return passwords

    def addUser(self, username, password, email):
        self.__cursor.execute('''
        INSERT INTO users (username, password, email)
        VALUES (?, ?, ?)
        ''', (username, password, email))
        self.__conn.commit()

    def addPassword(self, username, password):
        self.__cursor.execute('''
        INSERT INTO passwords (password, username)
        VALUES (?, ?)
        ''', (password, username))
        self.__conn.commit()

    def updatePassword(self, username, currPassword, newPassword):
        self.cursor.execute('''
        UPDATE passwords
        SET password = ?
        WHERE password = ? AND username = ?
        ''', (newPassword, currPassword, username))
        self.__conn.commit()

    def deletePassword(self, username, password):
        self.cursor.execute('''
        DELETE FROM passwords
        WHERE service = ? AND username = ?
        ''',(password, username))
        self.__conn.commit()