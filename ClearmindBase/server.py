from .clearmine import ClearMine
from typing import Tuple, Optional
from .dababaseOperator import sqlOperator
from typing import Tuple
import threading
import json

class Server:
    def __init__(self) -> None:
        #self.__data_queue = []
        #self.__lock = threading.Lock()
        self.__CM = ClearMine()
        self.__SQL = sqlOperator()


    def login(self, username : str, password : str) -> bool:
        data = self.__SQL.select_by_user(username)
        if data == None: return False
        return password == data['passwd']

    
    def register(self, code : str, username : str, password : str) -> bool:
        return self.__SQL.register(code, username, password)


    def click(self, x : int , y : int, username : str) -> Tuple[int, str, bool]:
        color_number = self.__CM.get_user_color_num(username)
        color_string = self.__CM.get_user_color_str(color_number)
        click_status = self.__CM.click(x, y, color_number)
        
        return click_status, color_string




    # def __clear_data_queue(self) -> None:
    #     self.__data_queue = []

    # def get_message(self) -> Optional[Tuple[str, Tuple[str, int]]]:
    #     if len(self.__data_queue) == 0: return None
    #     return self.__data_queue.pop(0)

    # def push_message(self, message : Tuple[str, Tuple[str, int]]) -> None:
    #     self.__lock.acquire()
    #     self.__data_queue.append(message)
    #     self.__lock.release()

    # def __message_checker(self, operation : str):
    #     if operation == 'login': return 1
    #     if operation == 'register': return 2
    #     if operation == 'click': return 3


    # def __auto_work(self) -> None:
    #     while True:
    #         message = self.get_message()
    #         if message:
    #             data, address = message
    #             data = json.loads()
    #             op = self.__message_checker(data['type'])
    #             pass
                


    # def working(self) -> None:
    #     t = threading.Thread(target = self.__auto_work, name = 'working')
    #     t.start()



