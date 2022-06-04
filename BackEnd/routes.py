from flask import (
    redirect,
    request,
    session,
    render_template,
    url_for,
    Blueprint,
    make_response,
)
from .objects import cookie_user_dict

clearmind_blueprint = Blueprint('main', __name__)


@clearmind_blueprint.route('/', methods=['GET', 'POST'])
def index():
    '''回馈login页面'''
    return render_template('login.html')

@clearmind_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    '''回馈register页面'''
    return render_template('register.html')

@clearmind_blueprint.route('/saolei', methods=['GET', 'POST'])
def mine():
    '''判断权限, 对有权限者回馈扫雷游戏页面'''
    res = '无权限'
    try:
        if request.args['uname'] in cookie_user_dict:
            res = make_response(render_template('saolei.html'))
        else:
            res += ', 请重新登录'
    except :
        pass
    return res

@clearmind_blueprint.route('/seealldata', methods=['GET', 'POST'])
def total_rank():
    '''判断权限, 对有权限者回馈扫雷战绩总榜页面'''
    res = '无权限'
    try:
        if request.args['uname'] in cookie_user_dict:
            res = make_response(render_template('seealldata.html'))
        else:
            res += ', 请重新登录'
    except :
        pass
    return res





