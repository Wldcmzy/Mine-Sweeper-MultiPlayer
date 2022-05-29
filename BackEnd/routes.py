from flask import (
    redirect,
    request,
    session,
    render_template,
    url_for,
    Blueprint,
    make_response,
)

clearmind_blueprint = Blueprint('main', __name__)


@clearmind_blueprint.route('/', methods=['GET', 'POST'])
def index():
    return render_template('login.html')

@clearmind_blueprint.route('/mine', methods=['GET', 'POST'])
def mine():
    print(request.headers)
    res = make_response(render_template('mine.html'))
    res.headers['cookie'] = 123456789
    return res

@clearmind_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('/mine')

@clearmind_blueprint.route('/wk', methods=['GET', 'POST'])
def _():
    return render_template('wk.html')



