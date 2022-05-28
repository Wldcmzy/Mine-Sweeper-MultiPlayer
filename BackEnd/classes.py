
from random import randint

class User:
    def __init__(self, username : str) -> None:
        self.__name = username
        self.__id = randint(10000000, 99999999)
        self.__temp = self.__name + str(self.__id)
        
    def get(self) -> str:
        return self.__temp