from src.app import app, FlaskConfig
from src.modules.permissions.models import Permission

if __name__ == '__main__':
    app.run(FlaskConfig.HOST, FlaskConfig.PORT, debug=FlaskConfig.DEBUG)
