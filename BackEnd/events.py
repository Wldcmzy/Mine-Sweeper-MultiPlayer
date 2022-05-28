from flask import session, request
from flask_socketio import emit, join_room, leave_room
from .objects import clearmind_socketio


@clearmind_socketio.on('connect', namespace='/call')
def connect():
    print('连接成功')
    session['abc'] = '123'
    print('s>>>', session)
    print('f>>>', request.args)
    print('f>>>', request.headers)
    print('f>>>', request)
    #print('>>>', current_user)
    emit('connect reply', '')

@clearmind_socketio.on('disconnect', namespace='/call')
def disconnect():
    print('连接断开')
    print('>>>', session)
    print('>>>', request)

@clearmind_socketio.on('A', namespace='/call')
def _(msg):
    print(type(msg), str(msg))

