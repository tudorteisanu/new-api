from api import app, FlaskConfig
from services.logs.logs import init_logging


if __name__ == '__main__':
    # init_logging(app)
    app.run(FlaskConfig.HOST, FlaskConfig.PORT, FlaskConfig.DEBUG)
