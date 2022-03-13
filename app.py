from src.app import app, socketio, FlaskConfig
from src.services.logs import init_logging

if __name__ == '__main__':
    if FlaskConfig.PRODUCTION:
        init_logging(app)

    socketio.run(app, FlaskConfig.HOST, FlaskConfig.PORT, debug=FlaskConfig.DEBUG)
