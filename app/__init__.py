from flask import Flask
from flask_socketio import SocketIO

app = Flask(__name__)

from app import routes
