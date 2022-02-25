from app import create_app, FlaskConfig
from services.logs.logs import init_logging

app = create_app()

if __name__ == '__main__':
    init_logging(app)
    app.run(FlaskConfig.HOST, FlaskConfig.PORT, FlaskConfig.DEBUG)
