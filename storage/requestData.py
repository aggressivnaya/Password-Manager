import base

class Request(base.Base):
    def __init__(self, connection, cursor):
        self.__conn = connection
        self.__cursor = cursor

    def add(self, userId, groupId ,command):
        try:
            self.__cursor.execute('''
                INSERT INTO requests(userId, requestCommand, groupId) VALUES(?, ?, ?)
                ''', (userId, command, groupId))
            self.__conn.commit()
            return True
        except Exception as e:
            print(f"Error insert request; {e}")
            return False
            

    def delete(self, adminId, groupId, command):
        try:
            self.__cursor.execute('''
                DELETE FROM requests WHERE userId = ? AND gorupId = ? AND requestCommand = ?
                ''', (adminId, groupId, command,))
            self.__conn.commit()
            return True
        except Exception as e:
            print(f"Error delete request: {e}")
            return False


    def getRequests(self, adminId, groupId):
        try:
            self.__cursor.execute('''
                SELECT * FROM requests WHERE userId = ? AND groupId = ?
                ''',(adminId, groupId,))
            
            requests = self.__cursor.fetchall()
            return list(requests)
        except Exception as e:
            print(f"Error getting list of requests of group: {e}")
            return False