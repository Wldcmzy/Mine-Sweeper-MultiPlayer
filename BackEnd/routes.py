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

@clearmind_blueprint.route('/saolei', methods=['GET', 'POST'])
def mine():
    print(request.headers)
    res = make_response(render_template('saolei.html'))
    return res





