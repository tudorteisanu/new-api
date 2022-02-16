from config.settings import create_app
from config.flask_config import FlaskConfig

app = create_app()

if __name__ == '__main__':
    app.run(FlaskConfig.HOST, FlaskConfig.PORT, FlaskConfig.DEBUG)
