
from flask import session, request
from flask_socketio import emit, join_room, leave_room, disconnect
from numpy import broadcast
from .objects import CM_server, clearmind_socketio, cookie_user_dict, DISCONNECT_TIME, user_cookie, gen_cookie
import time
import json


@clearmind_socketio.on('connect', namespace='/wslogin')
def login_connect():
    print('收到登录请求')
    try:
        print('asdklfjskljdasjflkasdhglkashl')
        print(request.args)
        username = request.args['username']
        password = request.args['password']
        print('>>>>>>>>>>>>>>>>>>>', username , password)
        '''进行身份识别, 返回cookie或错误信息'''

        if CM_server.login(username, password) == True:
            cookie = str(gen_cookie())
            if username in user_cookie:
                del cookie_user_dict[user_cookie[username]]
            user_cookie[username] = cookie
            cookie_user_dict[cookie] = (username, time.time())
            emit('reply', cookie)
            print('send  cookie <<<<<<<<<<<<')
        else:
            emit('reply', 'deny')
            print('send  deny <<<<<<<<<<<<')
    except Exception as e:
        login_disconnect()
        print('ERROR <<<<<<<<<<<<')
        print(type(e), str(e))
        return False

@clearmind_socketio.on('disconnect', namespace='/wslogin')
def login_disconnect():
    print('登录连接断开...')


@clearmind_socketio.on('connect', namespace='/wsregister')
def login_connect():
    print('注册登录请求')
    # try:
    invitecode = request.args['invitecode']
    username = request.args['username']
    password = request.args['password']
    print('>>>>>>>>>>>>>>>>>> ok11111')
    if CM_server.register(invitecode, username, password) == True:
        emit('reply', 'ok')
        print('>>>>>>>>>>>  send ok')
    else:
        emit('reply', 'deny')
        print('>>>>>>>>>>>  send deny')
    # except:
    #     register_disconnect()
    #     print('????????????????????')
    #     return False

@clearmind_socketio.on('disconnect', namespace='/wsregister')
def register_disconnect():
    print('注册连接断开...')


@clearmind_socketio.on('connect', namespace='/wsmine')
def mine_connect():
    print('>>>>>>>>扫雷连接成功')
    try:
        judge = False
        cookie = request.args['cookie']
        username = ''
        if cookie in cookie_user_dict:
            username, tm = cookie_user_dict[cookie]
            if time.time() - tm < DISCONNECT_TIME:
                judge = True
            else:
                del user_cookie[username]
                del cookie_user_dict[cookie]
        if not judge: 
            raise Exception('身份无效')
        CM_server.give_color(username)
        emit('args', json.dumps(CM_server.args()))
        emit('history', json.dumps(CM_server.history()))
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



@clearmind_socketio.on('click', namespace='/wsmine')
def mine_click(info):
    print('>>>>> clicked')
    if CM_server.ready() == False: return
    cookie = request.args['cookie']
    data = json.loads(info)
    x, y = data['x'], data['y']
    # username = data['username']
    username, tm = cookie_user_dict[cookie]
    # if time.time() - tm < DISCONNECT_TIME:
    #     return False
    print(x, y, username)
    snd, color, finish, timmer = CM_server.click(x, y, username)
    if snd:
        print(str(snd), color, str(finish), str(timmer))
        emit('broadcast', json.dumps({'x' : x, 'y' : y, 'color' : color, 'timmer' : timmer}), broadcast = True)
    if finish:
        CM_server.restart()
        emit('args', json.dumps(CM_server.args()), broadcast = True)
