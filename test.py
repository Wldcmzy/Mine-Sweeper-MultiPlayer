#!/bin/env python
from distutils.log import debug
from flask import Flask
from BackEnd.socket_def import clearmind_socketio
from BackEnd.routes import clearmind_blueprint


def create_app(debug = True):
    app = Flask(__name__)
    app.debug = debug
    app.config['SECRET_KEY'] = 'clearmind'
    app.register_blueprint(clearmind_blueprint)
    clearmind_socketio.init_app(app)
    from BackEnd import events
    return app


if __name__ == '__main__':
    app = create_app()

    clearmind_socketio.run(app, host='0.0.0.0', port=26666)


