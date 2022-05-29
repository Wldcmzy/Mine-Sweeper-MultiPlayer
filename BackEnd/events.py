from flask import session, request
from flask_socketio import emit, join_room, leave_room, disconnect
from .objects import clearmind_socketio, cookie_user_dict, DISCONNECT_TIME, user_cookie
import time
import json



@clearmind_socketio.on('connect', namespace='/wslogin')
def login_connect():
    print('收到登录请求')
    try:
        username = request.args['username']
        password = request.args['password']
        '''进行身份识别, 返回cookie或错误信息'''
        cookie = '123'
        if True:
            if username in user_cookie:
                del cookie_user_dict[user_cookie[username]]
            user_cookie[username] = cookie
            cookie_user_dict[cookie] = (username, time.time())
            emit('reply', cookie)
        else:
            emit('reply', 'deny')
    except:
        login_disconnect()
        return False

@clearmind_socketio.on('disconnect', namespace='/wslogin')
def login_disconnect():
    print('登录连接断开...')


@clearmind_socketio.on('connect', namespace='/wsregister')
def login_connect():
    print('注册登录请求')
    try:
        invitecode = request.args['invitecode']
        username = request.args['username']
        password = request.args['password']
        '''注册'''
        emit('reply', '!!!!!!')
    except:
        register_disconnect()
        return False

@clearmind_socketio.on('disconnect', namespace='/wsregister')
def register_disconnect():
    print('注册连接断开...')


@clearmind_socketio.on('connect', namespace='/wsmine')
def mine_connect():
    print('扫雷连接成功')
    try:
        judge = False
        cookie = request.args['cookie']
        if cookie in cookie_user_dict:
            username, tm = cookie_user_dict[cookie]
            if time.time() - tm < DISCONNECT_TIME:
                judge = True
            else:
                del user_cookie[username]
                del cookie_user_dict[cookie]
        if not judge: 
            raise Exception('身份过期')
    except :
        mine_disconnect()
        return False


@clearmind_socketio.on('disconnect', namespace='/wsmine')
def mine_disconnect():
    cookie = request.args['cookie']
    username, tm = cookie_user_dict[cookie]
    del user_cookie[username]
    del cookie_user_dict[cookie]
    print('扫雷连接断开')


