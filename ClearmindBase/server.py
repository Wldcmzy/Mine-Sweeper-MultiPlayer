from .clearmine import ClearMine
from typing import Tuple, Optional
import threading
import json

class Server:
    def __init__(self) -> None:
        #self.__data_queue = []
        #self.__lock = threading.Lock()
        self.__CM = ClearMine()
        self.__SQL = None

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



