from flask import (
    redirect,
    request,
    session,
    render_template,
    url_for,
    Blueprint,
)

clearmind_blueprint = Blueprint('main', __name__)


@clearmind_blueprint.route('/', methods=['GET', 'POST'])
def index():
    return render_template('login.html')

@clearmind_blueprint.route('/mine', methods=['GET', 'POST'])
def mine():
    print(request.headers)
    return render_template('mine.html')

@clearmind_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('/mine')



