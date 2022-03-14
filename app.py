from src.app import app, FlaskConfig
from src.services.logs import init_logging
from dotenv import load_dotenv

if __name__ == '__main__':
    if FlaskConfig.PRODUCTION:
        init_logging(app)
    load_dotenv('.env')
    app.run(FlaskConfig.HOST, FlaskConfig.PORT, debug=FlaskConfig.DEBUG)
