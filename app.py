from src.app import app, FlaskConfig
from src.services.logs import init_logging

if __name__ == '__main__':
    if FlaskConfig.PRODUCTION:
        init_logging(app)
    app.run(FlaskConfig.HOST, FlaskConfig.PORT, debug=FlaskConfig.DEBUG)
