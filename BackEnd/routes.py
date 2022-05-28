from flask import (
    redirect,
    request,
    session,
    render_template,
    url_for,
    Blueprint,
)

clearmind_blueprint = Blueprint('main', __name__)


@clearmind_blueprint.route('/', methods=['GET'])
def index():
    return render_template('login.html')

@clearmind_blueprint.route('/mine')
def mine():
    return render_template('mine.html')

@clearmind_blueprint.route('/login')
def login():
    return redirect('/mine')



