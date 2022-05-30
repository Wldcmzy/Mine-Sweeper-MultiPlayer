from flask_socketio import SocketIO
from typing import Dict, Tuple
from random import randint

import sys
sys.path.append("..")
from ClearmindBase import Server
# from ..ClearmindBase import Server

clearmind_socketio = SocketIO()
cookie_user_dict : Dict[str, Tuple[str, float]] = {}
user_cookie : Dict[str, str] = {}
DISCONNECT_TIME = 300

CM_server = Server()

def gen_cookie():
    cookie = randint(10000000000000000000, 9999999999999999999999999)
    while True:
        if cookie not in cookie_user_dict: break
        cookie = randint(10000000000000000000, 9999999999999999999999999)
    return cookie
        

