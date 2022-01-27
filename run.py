from config.settings import app
from config.flask_config import FlaskConfig


if __name__ == '__main__':
    import urls

    app.run(FlaskConfig.HOST, FlaskConfig.PORT, FlaskConfig.DEBUG)
