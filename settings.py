from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_cors import CORS
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_socketio import SocketIO
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from flask_mail import Mail
# import redis as Redis

app = Flask(__name__)

api = Api(app)

app.config['SECRET_KEY'] = 'mysecret'
socketio = SocketIO(app)
jwt = JWTManager(app)
CORS(app)
app.config.from_object('config.FlaskConfig')
db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)
ma = Marshmallow(app)
mail = Mail(app)

# redis = Redis.StrictRedis(host='127.0.0.1', port=6379, db=2)