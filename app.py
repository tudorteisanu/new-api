from src.app import app, FlaskConfig
from src.services.logs import init_logging
from src.services.http.permissions import save_permissions_to_file


if __name__ == '__main__':
    if FlaskConfig.PRODUCTION:
        init_logging(app)
    save_permissions_to_file()
    app.run(FlaskConfig.HOST, FlaskConfig.PORT, debug=FlaskConfig.DEBUG)
