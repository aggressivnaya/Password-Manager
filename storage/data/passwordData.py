import EncryptionDecryption as e
import datetime
import base

class Password(base.Base):
    def __init__(self, connection, cursor):
        self.__conn = connection
        self.__cursor = cursor

    def findId(self, password):
        '''
        finding password id by the password
        '''
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
        
    def findPassword(self, passwordId):
        '''
        finding the password by the id
        '''
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
        
    def findId(self, userId):
        '''
        finding the password id by user id
        '''
        try:
            self.__cursor.execute('''
                SELECT passwordId FROM usersPasswords WHERE userId = ?''', (userId,)
            )
            passwordId = self.__cursor.fetchall() 
            if passwordId: #TODO
                return list(passwordId)  # Return the password id
            else:
                return None 
        except Exception as e:
            print(f"An error occurred while finding user ID by username: {e}")
            return None
        
    def getUserPasswords(self, userId):
        try:
            self.__cursor.execute('''
                SELECT p.id, p.name, p.password FROM passwords p
                JOIN usersPasswords up ON p.id = up.passwordId
                WHERE up.userId = ?''', 
                (userId,)
            )
            passwords = self.__cursor.fetchall()
            if passwords:
                passwordMetadata = [
                {
                    'id': row[0],
                    'name': row[1],
                    'password': row[2],
                    'shared': row[3]
                }
                for row in passwords
            ]
                #decodedPasswords = []
                #for i in passwords:
                 #   decodedPasswords.append(str(e.decryption(i)))
                return passwordMetadata
            else:
                return []
        except Exception as e:
            print(f"An error occurred while fetching passwords for user: {e}")
            return []
        
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
            
            sharedPassMetadata = [
                {
                    'id': row[0],
                    'name': row[1],
                    'password': row[2],
                    'shared': row[3]
                }
                for row in requests
            ]
            return sharedPassMetadata
        except Exception as e:
            print(f"Error with getting shared passwords: {e}")
            return False
        
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
    
    def add(self, userId, name, password, isShared):
        try:
            #encryptedPassword = e.encryption(password)
            self.__cursor.execute('''
                INSERT INTO passwords (name, password, shared) VALUES (?, ?, ?)''', 
                (name, password, isShared)
            )
            self.__conn.commit()
            print(f"Password {name} added successfully.")
            #userId = self.findUserIdByUsername(username)
            passwordId = self.findId(password)
            self.assignPasswordToUser(userId, passwordId)
            self.add(userId, passwordId, "ADD")
            return True
        except Exception as e:
            print(f"An error occurred while adding password: {e}")
            return False

    def update(self, userId, passwordId, newName, newPassword, isShared):
        try:
            #newEncryptedPassword = e.encryption(newPassword)
            self.__cursor.execute('''
                UPDATE passwords SET name = ?, password = ?, shared = ? WHERE id = ?''', 
                (newName, newPassword, isShared, passwordId)
            )
            self.__conn.commit()
            print(f"Password with ID {passwordId} updated successfully.")
            #userId = self.findUserIdByUsername(username)
            self.add(userId, passwordId, "UPDATE")
            return True
        except Exception as e:
            print(f"An error occurred while updating password: {e}")
            return False

    def delete(self, userId, passwordId):
        try:
            self.__cursor.execute('''
                DELETE FROM passwords WHERE id = ?''', 
                (passwordId,)
            )
            self.__conn.commit()
            print(f"Password with ID {passwordId} deleted successfully.")
            #userId = self.findUserIdByUsername(username)
            self.__cursor.execute('''
                DELETE FROM usersPasswords WHERE userId = ? AND passwordId = ?''', 
                (userId, passwordId,)
            )
            self.__conn.commit()

            self.add(userId, passwordId, "DELETE")
            return True
        except Exception as e:
            print(f"An error occurred while deleting password: {e}")
            return False

    def add(self, passwordId, method):
        '''
        the func is saving to history the change that was made
        '''
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
        
    def getHistory(self, userId):
        passwordsIds = self.findId(userId)
        historyOfAllPasswords = []
        try:
            for password in passwordsIds:
                self.__cursor.execute('''
                    SELECT * FROM history WHERE passwordId = ? ORDER BY date DESC
                    LIMIT 5
                    ''', (password,))
                result = self.__cursor.fetchall()
                if result:
                    historyOfAllPasswords = [
                        {
                            'id': row[0],
                            'name': row[1],
                            'password': row[2]
                        }
                        for row in result
                    ]
                else:
                    continue
            return historyOfAllPasswords
        except Exception as e:
            print(f"Error getting the history of the user: {e}")
            return None

    '''def getPasswordNameById(self, passwordId):
        try:
            self.__cursor.execute(
                SELECT name
                FROM passwords
                WHERE id = ?
            , (passwordId,))
            
            result = self.__cursor.fetchone()
            
            if result:
                return result[0]  # Returning the name (first column in result)
            else:
                return None  # No password found with the given ID
        
        except Exception as e:
            print(f"Error retrieving password name: {e}")
            return None'''