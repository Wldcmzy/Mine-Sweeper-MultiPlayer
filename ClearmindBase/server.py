
from .clearmine import ClearMine
from typing import Tuple, Optional
from .databaseOperator import sqlOperator
from typing import Tuple
import threading
import json
import time

class Server:
    def __init__(self) -> None:
        #self.__data_queue = []
        #self.__lock = threading.Lock()
        self.__CM = ClearMine()
        self.__SQL = sqlOperator()
        self.__SQL.active()
        self.__ready = 0


    def login(self, username : str, password : str) -> bool:
        data = self.__SQL.select_by_user(username)
        if data == None: return False
        return password == data['passwd']

    
    def register(self, code : str, username : str, password : str) -> bool:
        return self.__SQL.register(code, username, password)


    def click(self, x : int , y : int, username : str) -> Tuple[bool, str, bool, int]:
        color_number = self.__CM.get_user_color_num(username)
        color_string = self.__CM.get_user_color_str(color_number)
        click_status = self.__CM.click(x, y, color_number)
        finish = self.__CM.judge_win()

        bool_ret = False
        if click_status >= 0:
            clearCount = self.__SQL.select_userInfo_clearCount(username)
            self.__SQL.update_userInfo_clearCount(username, clearCount + click_status)
            bool_ret = True
        elif click_status == -1:
            boomCount = self.__SQL.select_userInfo_boomCount(username)
            self.__SQL.update_userInfo_boomCount(username, boomCount + 1)
            bool_ret = True

        return bool_ret, color_string, finish, self.__CM.get_timmer()

    def timmer(self):
        return self.__CM.get_timmer()

    def history(self):
        return self.__CM.get_click_history()

    def args(self):
        return self.__CM.get_args()

    def restart(self):
        self.__CM.restart(True)
        self.__ready = time.time()

    def ready(self):
        return time.time() > self.__ready