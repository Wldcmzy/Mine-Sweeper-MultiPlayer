#!/bin/env python
from flask import Flask
from BackEnd.objects import clearmind_socketio, login_manager
from BackEnd.routes import clearmind_blueprint
from flask_login import LoginManager


def create_app(debug = True):
    app = Flask(__name__)
    app.debug = debug
    app.config['SECRET_KEY'] = 'clearmind'
    app.register_blueprint(clearmind_blueprint)
    clearmind_socketio.init_app(app)
    # login_manager.init_app(app)
    # login_manager.login_view = 'login'
    from BackEnd import events
    return app


if __name__ == '__main__':
    app = create_app()
    clearmind_socketio.run(app, host='0.0.0.0', port=26666)


