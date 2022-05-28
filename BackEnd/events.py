from flask import session
from flask_socketio import emit, join_room, leave_room
from .socket_def import clearmind_socketio

@clearmind_socketio.on('connect', namespace='/call')
def connect():
    print('连接成功')

@clearmind_socketio.on('disconnect', namespace='/call')
def disconnect():
    print('连接断开')

@clearmind_socketio.on('A', namespace='/call')
def _(msg):
    print(type(msg), str(msg))

