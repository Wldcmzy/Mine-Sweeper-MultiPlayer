from time import time
import pymysql
class sqlOperator:
    def __init__(self, host, user, password, database):
        self.__host = host
        self.__user = user
        self.__password = password
        self.__database = database
    
    # 激活对象
    def active(self):
        self.__connection = pymysql.connect(host = self.__host, user = self.__user, password = self.__password, database = self.__database)
        self.__cursor = self.__connection.cursor(cursor=pymysql.cursors.DictCursor)

    # 关闭对象功能
    def inactive(self):
        self.__connection.close()
        self.__cursor.close()

    def select_invitation_userID(self, invitationCode):
        sql = 'select userID from invitation where invitationCode = \'%s\'' % (invitationCode)
        self.__cursor.execute(sql)
        ret = self.__cursor.fetchone()
        return ret

    def select_invitation_ifUsed(self, invitationCode):
        sql = 'select ifUsed from invitation where invitationCode = \'%s\'' % (invitationCode)
        self.__cursor.execute(sql)
        ret = self.__cursor.fetchone()
        return ret

    def update_invitation_ifUsed(self, invitationCode, ifUsed):
        sql = 'update invitation set ifUsed = %d where invitationCode = \'%s\'' % (ifUsed,invitationCode)
        self.__cursor.execute(sql)
        self.__connection.commit()

    def select_userInfo_uAp(self, userID):
        sql = 'select username,passwd from userInfo where userID = \'%s\'' % (userID)
        self.__cursor.execute(sql)
        ret = self.__cursor.fetchone()
        return ret
    
    def update_userInfo_uAp(self, userID, dir):
        sql = 'update userInfo set username = \'%s\' , passwd = \'%s\' where userID = \'%s\'' % (dir['username'],dir['password'],userID)
        self.__cursor.execute(sql)
        self.__connection.commit()
    
    def select_userInfo_ifOnline(self, userID):
        sql = 'select ifOnline from userInfo where userID = \'%s\'' % (userID)
        self.__cursor.execute(sql)
        ret = self.__cursor.fetchone()
        return ret
    
    def update_userInfo_ifOnline(self, userID, ifOnline):
        sql = 'update userInfo set ifOnline = %d where userID= \'%s\'' % (ifOnline,userID)
        self.__cursor.execute(sql)
        self.__connection.commit()

    def select_userInfo_clearCount(self, userID):
        sql = 'select clearCount from userInfo where userID = \'%s\'' % (userID)
        self.__cursor.execute(sql)
        ret = self.__cursor.fetchone()
        return ret
    
    def update_userInfo_clearCount(self, userID, clearCount):
        sql = 'update userInfo set clearCount = %d where userID= \'%s\'' % (clearCount,userID)
        self.__cursor.execute(sql)
        self.__connection.commit()

    def select_userInfo_boomCount(self, userID):
        sql = 'select boomCount from userInfo where userID = \'%s\'' % (userID)
        self.__cursor.execute(sql)
        ret = self.__cursor.fetchone()
        return ret
    
    def update_userInfo_boomCount(self, userID, boomCount):
        sql = 'update userInfo set boomCount = %d where userID= \'%s\'' % (boomCount,userID)
        self.__cursor.execute(sql)
        self.__connection.commit()

    
