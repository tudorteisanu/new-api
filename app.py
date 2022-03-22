from src.app import app, FlaskConfig
from src.services.logs import init_logging


if FlaskConfig.PRODUCTION:
    init_logging(app)

if not FlaskConfig.PRODUCTION:
    if __name__ == '__main__':
        app.run(FlaskConfig.HOST, FlaskConfig.PORT, debug=FlaskConfig.DEBUG)
