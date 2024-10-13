import EncryptionDecryption as e

class Group():
    def __init__(self, connection, cursor):
        self.__conn = connection
        self.__cursor = cursor

    def create(self, adminId, name, description):
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
        
    def accept(self, adminId, userId, groupId):
        if self.checkAdmin(groupId, adminId):
            self.enter(userId, groupId)
            return True
        else:
            return False
        
    def enter(self, userId, groupId, isAdmin=False):
        try:
            self.__cursor.execute('''
                INSERT INTO usersGroups(userId, isAdmin, groupId) VALUES(?, ?, ?)
                ''',(userId, isAdmin, groupId))
            self.__conn.commit()
            return True
        except Exception as e:
            print(f"Error with entering the group: {e}")
            return False
    
    def leave(self, userId, groupId):
        try:
            self.__cursor.execute('''
                DELETE FROM usersGroups WHERE userId = ? AND groupId = ?
                ''', (userId, groupId))
            self.__conn.commit()
            return True
        except Exception as e:
            print(f"Error with leaving the group: {e}")
            return False

    def removeUser(self, adminId, userId, groupId):
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
            if not self.checkAdmin(groupId, adminId):
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
        
    def getInfo(self, groupId):
        try:
            self.__cursor.execute('''
                SELECT * FROM groups WHERE id = ?
                ''', (groupId,))
            
            requests = self.__cursor.fetchall()

            groupMetadata = [
                {
                    'id': row[0],
                    'name': row[1],
                    'description': row[2],
                }
                for row in requests
            ]
            return groupMetadata
        except Exception as e:
            print(f"Error with getting the info of the group: {e}")
            return False