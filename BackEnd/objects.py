from flask_socketio import SocketIO
from typing import Dict, Tuple

clearmind_socketio = SocketIO()
cookie_user_dict : Dict[str, Tuple[str, float]] = {}
user_cookie : Dict[str, str] = {}
DISCONNECT_TIME = 300