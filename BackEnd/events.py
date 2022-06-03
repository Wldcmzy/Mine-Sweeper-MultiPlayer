import threading
from flask import session, request
from flask_socketio import emit, join_room, leave_room, disconnect
from .objects import (
    CM_server, 
    clearmind_socketio, 
    cookie_user_dict, 
    DISCONNECT_TIME, 
    user_cookie, 
    gen_cookie,
    SERVER_WAIT_TIME,
)
import time
import json

@clearmind_socketio.on('connect', namespace='/wslogin')
def login_connect():
    '''收到登录请求,进行身份识别, 发送cookie或拒绝信息'''
    print('收到登录请求...')
    try:
        username = request.args['username']
        password = request.args['password']

        # 先判断账号密码是否正确
        if CM_server.login(username, password) == True:
            # 生成cookie
            cookie = None
            while True:
                cookie = str(gen_cookie())
                if cookie not in cookie_user_dict:
                    break

            # 如果用户多次登录, 撤销用户先前的cookie, 设置cookie, 并设置最近活跃时间
            if username in user_cookie:
                del cookie_user_dict[user_cookie[username]]
            user_cookie[username] = cookie
            cookie_user_dict[cookie] = (username, time.time())

            emit('reply', cookie)
        else:
            emit('reply', 'deny')
    except Exception as e:
        login_disconnect()
        print(str(type(e)), str(e))
        return False

@clearmind_socketio.on('disconnect', namespace='/wslogin')
def login_disconnect():
    '''登录连接断开时执行'''
    extra = ''
    try : 
        username = request.args['username']
        password = request.args['password']
        extra = username
    except:
        pass
    print(f'登录连接断开...   {username}')


@clearmind_socketio.on('connect', namespace='/wsregister')
def login_connect():
    '''收到登录请求后, 进行登录操作, 并发送事务结果'''
    print('注册登录请求')
    try:
        invitecode = request.args['invitecode']
        username = request.args['username']
        password = request.args['password']
        register_ret = CM_server.register(invitecode, username, password)
        if register_ret == True:
            emit('reply', 'ok')
        elif register_ret is None:
            emit('reply', 'script')
        else:
            emit('reply', 'deny')
    except Exception as e:
        register_disconnect()
        print(str(type(e)), str(e))
        return False

@clearmind_socketio.on('disconnect', namespace='/wsregister')
def register_disconnect():
    '''登录链接断开后执行'''
    print('注册连接断开...')


@clearmind_socketio.on('connect', namespace='/wsmine')
def mine_connect():
    print('===> 扫雷连接成功...')
    try:
        judge = False
        cookie = request.args['cookie']
        username = ''
        print('2')
        if cookie in cookie_user_dict:
            username, tm = cookie_user_dict[cookie]
            if time.time() - tm < DISCONNECT_TIME:
                judge = True
            else:
                del user_cookie[username]
                del cookie_user_dict[cookie]
        if not judge: 
            raise Exception('身份过期')
        print('1')
        emit('args', json.dumps(CM_server.args()))
        emit('history', json.dumps(CM_server.history()))
    except Exception as e:
        mine_disconnect()
        print(str(type(e)) + str(e))
        return False


@clearmind_socketio.on('disconnect', namespace='/wsmine')
def mine_disconnect():
    '''扫雷链接断开时, 注销用户cookie'''
    try:
        cookie = request.args['cookie']
        username, tm = cookie_user_dict[cookie]
        del user_cookie[username]
        del cookie_user_dict[cookie]
    except:
        pass
    print('扫雷连接断开...')



@clearmind_socketio.on('click', namespace='/wsmine')
def mine_click(info):
    '''收到点击地图时间, 把数据中的参数抛给后端处理'''

    # # 若服务器ready码为假, 发送拒绝信息
    # if not CM_server.ready():
    #     emit('error', 'not ready')
    #     return False

    try :
        cookie = request.args['cookie']
        data = json.loads(info)
        x, y = data['x'], data['y']
        username, tm = cookie_user_dict[cookie]
    except Exception as e:
        print(str(type(e)), str(e))
        return False

    # 判断身份是否过期
    if time.time() - tm > DISCONNECT_TIME: 
        emit('error', 'gone too long')
        return False

    CM_server.give_color(username)
    snd, color, finish, timmer = CM_server.click(x, y, username)
    # 更新最近活跃时间
    cookie_user_dict[cookie] = (username, time.time())
    if snd:
        print(f'广播{x} {y} {color} {username}' )
        emit('broadcast', json.dumps({'x' : x, 'y' : y, 'color' : color, 'timmer' : timmer, 'username' : username}), broadcast = True)
        print('已经发完')
    if finish:
        emit('broadcast finish', 'finish', broadcast = True)
        # 可能在架构原理上存在一些问题, 暂时不开启一局结束后等待一段时间的功能
        # CM_server.restart(SERVER_WAIT_TIME)
        CM_server.restart()
        while not CM_server.ready(): pass
        emit('game end', '', broadcast = True)
        emit('args', json.dumps(CM_server.args()), broadcast = True)


@clearmind_socketio.on('rank', namespace='/wsmine')
def getrank(info):
    '''发送查询到的本局战绩信息'''
    try :
        if info != 'query rank': return False
        cookie = request.args['cookie']
        username, tm = cookie_user_dict[cookie]

        # 判断身份是否过期
        if time.time() - tm > DISCONNECT_TIME: 
            emit('error', 'gone too long')
            return False

        cookie_user_dict[cookie] = (username, time.time())
    except Exception as e:
        print(str(type(e)), str(e))
        return False

    emit('rank_rev', json.dumps(CM_server.rank()))

@clearmind_socketio.on('connect', namespace='/wsrank')
def rank_connect():
    print('查看总榜链接成功...')

@clearmind_socketio.on('disconnect', namespace='/wsrank')
def rank_connect():
    print('查看总榜链接断开...')

@clearmind_socketio.on('total_rank', namespace='/wsrank')
def get_total_rank(info):
    '''发送查询到的战绩总榜信息'''
    try : 
        if info != 'query rank': return False
        cookie = request.args['cookie']
        username, tm = cookie_user_dict[cookie]

        # 判断身份是否过期
        if time.time() - tm > DISCONNECT_TIME: 
            emit('error', 'gone too long')
            return False

        cookie_user_dict[cookie] = (username, time.time())
        ttt = CM_server.total_rank()
        print('send...' + str(ttt))
        emit('total_rank', json.dumps(ttt))
    except Exception as e:
        print(type(e), str(e))