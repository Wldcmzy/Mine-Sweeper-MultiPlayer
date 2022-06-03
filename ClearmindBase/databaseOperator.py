from random import randint
import pymysql
#from soupsieve import select
from .config import HOST, USER, PASSWORD, DATABASE
from typing import Dict, Optional, List
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

    # 查询邀请码对应的userID
    def select_invitation_userID(self, invitationCode) -> Optional[dict]:
        sql = 'select userID from invitation where invitationCode = \'%s\'' % (invitationCode)
        self.__cursor.execute(sql)
        ret = self.__cursor.fetchone()
        return ret

    # 查询邀请码是否被使用过
    # -1 表示邀请码错误 运行正常返回0或1
    def select_invitation_ifUsed(self, invitationCode) -> int:
        sql = 'select ifUsed from invitation where invitationCode = \'%s\'' % (invitationCode)
        self.__cursor.execute(sql)
        ret = self.__cursor.fetchone()
        if ret == None:
            return -1
        else:
            return ret['ifUsed']

    # 更新邀请码使用记录
    # -1表示邀请码错误  运行正常返回1
    def update_invitation_ifUsed(self, invitationCode, ifUsed) -> int:
        sql = 'update invitation set ifUsed = %d where invitationCode = \'%s\'' % (ifUsed,invitationCode)
        ret = self.__cursor.execute(sql)
        self.__connection.commit()
        if ret == 0:
            return -1
        else:
            return ret
    
    # 查询用户名和密码
    def select_userInfo_uAp(self, userID) -> Optional[dict]:
        sql = 'select username,passwd from userInfo where userID = \'%s\'' % (userID)
        self.__cursor.execute(sql)
        ret = self.__cursor.fetchone()
        return ret

    # 更新用户名和密码
    # -2表示userID错误  运行正常返回1
    def update_userInfo_uAp(self, userID, dir) -> int:
        sql = 'update userInfo set username = \'%s\' , passwd = \'%s\' where userID = \'%s\'' % (dir['username'],dir['passwd'],userID)
        ret = self.__cursor.execute(sql)
        self.__connection.commit()
        if ret == 0:
            return -2
        else:
            return ret

    # 插入新用户
    # -3表示插入新用户异常  运行正常返回1
    def insert_serInfo_uAp(self,dir) -> int:
        sql = 'insert into userInfo values (\'%s\', \'%s\', \'%s\', 0, 0, 0)' % (dir['userID'] , dir['username'] , dir['passwd'])
        ret=self.__cursor.execute(sql)
        self.__connection.commit() 
        if ret == 0:
            return -3
        else:
            return ret

    # 查询用户是否在线
    # -4表示username错误  运行正常返回0或1
    def select_userInfo_ifOnline(self, username) -> int:
        sql = 'select ifOnline from userInfo where username = \'%s\'' % (username)
        self.__cursor.execute(sql)
        ret = self.__cursor.fetchone()
        if ret == None:
            return -4
        return ret['ifOnline']

    # 更改用户是否在线
    # -4表示username错误  运行正常返回1
    def update_userInfo_ifOnline(self, username, ifOnline) -> int:
        sql = 'update userInfo set ifOnline = %d where username= \'%s\'' % (ifOnline,username)
        ret = self.__cursor.execute(sql)
        self.__connection.commit()
        if ret == 0:
            return -4
        else:
            return ret
    
    # 查询用户扫出的区域个数
    # -4表示username错误 
    def select_userInfo_clearCount(self, username) -> int:
        sql = 'select clearCount from userInfo where username = \'%s\'' % (username)
        self.__cursor.execute(sql)
        ret = self.__cursor.fetchone()
        if ret == None:
            return -4
        else:
            return ret['clearCount']
    
    # 更新用户扫出的区域个数
    # -4表示username错误  运行正常返回1
    def update_userInfo_clearCount(self, username, clearCount) -> int:
        sql = 'update userInfo set clearCount = %d where username= \'%s\'' % (clearCount,username)
        ret = self.__cursor.execute(sql)
        self.__connection.commit()
        if ret == 0:
            return -4
        else:
            return ret

    # 查询用户炸雷个数
    # -4表示username错误 
    def select_userInfo_boomCount(self, username) -> int:
        sql = 'select boomCount from userInfo where username = \'%s\'' % (username)
        self.__cursor.execute(sql)
        ret = self.__cursor.fetchone()
        if ret == None:
            return -4
        else:
            return ret['boomCount']

    # 更新用户炸雷个数
    # -4表示username错误 
    def update_userInfo_boomCount(self, username, boomCount):
        sql = 'update userInfo set boomCount = %d where username= \'%s\'' % (boomCount,username)
        ret = self.__cursor.execute(sql)
        self.__connection.commit()
        if ret == 0:
            return -4
        else:
            return ret

    def add_invite_code(self, number: int) -> None:
        '''批量增加邀请码'''
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

    def get_invite_code(self) -> None:
        sql = 'select userID uid, invitationCode code from invitation where ifUsed = 0 order by uid'
        self.__cursor.execute(sql)
        return self.__cursor.fetchall()

    def select_by_user(self, username : str) -> Optional[dict]:
        '''根据用户名查询匹配者的所有信息'''
        sql = f'select * from userInfo where username = \'{username}\''
        self.__cursor.execute(sql)
        return self.__cursor.fetchone()

    def register(self, invitecode : str, username : str, password : str) -> bool:
        '''用户注册'''

        # 检查重名
        if self.select_by_user(username) != None: return False

        # 检查邀请码合法性(存在/未使用)
        sql = f'select userID, ifUsed from invitation where invitationCode = \'{invitecode}\''
        row = self.__cursor.execute(sql)
        if row == 0: return False
        data = self.__cursor.fetchone()
        if data['ifUsed'] != 0: return False

        # 注册操作
        sql = 'insert into userInfo values (%s, %s, %s, 0, 0, 0)'
        self.__cursor.execute(sql, (data['userID'], username, password))
        self.__connection.commit()
        self.update_invitation_ifUsed(invitecode, 1)
        return True

    def get_totalRank_data(self) -> Optional[List[dict]]:
        '''查询总榜(所有用户)信息'''

        sql = 'select username, clearCount, boomCount from userInfo'
        self.__cursor.execute(sql)
        return self.__cursor.fetchall()

    def test_select(self):
        '''测试使用, 无实际用途'''
        sql = 'select userID uid, invitationCode code from invitation'
        row = self.__cursor.execute(sql)
        return self.__cursor.fetchall()