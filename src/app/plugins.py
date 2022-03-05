from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_cors import CORS
from flask_migrate import Migrate
from flask_socketio import SocketIO
from flask_jwt_extended import JWTManager
from src.app.config import FlaskConfig


app = Flask(__name__, template_folder='../templates', static_folder="../static")
app.config.from_object(FlaskConfig)
api = Api(app, catch_all_404s=True, prefix='/api/v1')
socketio = SocketIO(app)
jwt = JWTManager(app)
CORS(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
db.init_app(app)

