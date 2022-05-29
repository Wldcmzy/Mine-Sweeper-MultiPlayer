from random import randint
import pymysql
from .config import HOST, USER, PASSWORD, DATABASE
class sqlOperator:
    def __init__(self, host = HOST, user = USER, password = PASSWORD, database = DATABASE):
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

    def add_invite_code(self, number: int) -> None:
        sql = 'select userID uid, invitationCode code from invitation'
        row = self.__cursor.execute(sql)
        datas = self.__cursor.fetchall()
        spanl, spanr = 10000, 99999
        for _ in range(number):
            row += 1
            code = str(row)
            for __ in range(5):
                code += '-' + str(randint(spanl, spanr))
            sql = 'insert into invitation values (%s, %s, 0);'
            self.__cursor.execute(sql, (row, code))
        self.__connection.commit()

    def select_by_user(self, username : str):
        sql = f'select * from userInfo where username = \'{username}\''
        self.__cursor.execute(sql)
        return self.__cursor.fetchone()

    def register(self, invitecode : str, username : str, password : str) -> bool:
        sql = f'select userID, ifUsed from invitation where invitationCode = \'{invitecode}\''
        row = self.__cursor.execute(sql)
        if row == 0: return False
        data = self.__cursor.fetchone()
        if data['ifUsed'] != 0: return False
        sql = 'insert into userInfo values (%s, %s, %s, 0, 0, 0)'
        self.__cursor.execute(sql, (data['userID'], username, password))
        self.__connection.commit()
        self.update_invitation_ifUsed(invitecode, 1)
        return True

    def test_select(self):
        sql = 'select userID uid, invitationCode code from invitation'
        row = self.__cursor.execute(sql)
        return self.__cursor.fetchall()