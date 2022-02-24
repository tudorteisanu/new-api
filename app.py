from config.settings import create_app
from config.flask_config import FlaskConfig
from services.logs import init_logging

app = create_app()

init_logging(app)
if __name__ == '__main__':
    app.run(FlaskConfig.HOST, FlaskConfig.PORT, FlaskConfig.DEBUG)
