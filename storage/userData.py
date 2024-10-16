import EncryptionDecryption as e
import base

class User(base.Base):
    def __init__(self, connection, cursor):
        self.__conn = connection
        self.__cursor = cursor

    def findId(self, username):
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
        
    def doesUserExist(self, username) -> bool:
        self.__cursor.execute('''
        SELECT id FROM users
        WHERE username = ?''', (username,))
        users = self.__cursor.fetchall()

        return len(users) > 0
    
    def add(self, username, email):
        try:
            self.__cursor.execute('''
                INSERT INTO users (username, email) VALUES (?, ?)''', 
                (username, email)
            )
            self.__conn.commit()
            print(f"User {username} added successfully.")
        except Exception as e:
            print(f"An error occurred while adding user: {e}")

    def logout(self, userId):
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
                ''', (userId,))
            self.__conn.commit()

            print("deleting other stuff")
            self.__cursor.execute('''
                DELETE FROM users WHERE id = ?
                ''', (userId,))
            self.__conn.commit()   
            return True
        except Exception as e:
            print(f"Error with logout: {e}")
            return False
        
    