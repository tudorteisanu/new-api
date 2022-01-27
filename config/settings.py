from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_cors import CORS
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_socketio import SocketIO
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from config.flask_config import FlaskConfig
from flask_login import LoginManager
# import redis as Redis

app = Flask(__name__, template_folder='../templates', static_folder="../static")
app.config.from_object(FlaskConfig)
api = Api(app, catch_all_404s=True, prefix='/api/v1')
socketio = SocketIO(app)
jwt = JWTManager(app)
CORS(app)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)
ma = Marshmallow(app)

# redis = Redis.StrictRedis(host='127.0.0.1', port=6379, db=2)
