import os

from src.app import app, FlaskConfig
from src.services.logs import init_logging
from src.services.http.permissions import check_permissions

if FlaskConfig.PRODUCTION:
    init_logging(app)

if __name__ == '__main__':
    os.system('flask db upgrade')
    os.system('python seeder.py')
    check_permissions()
    app.run(FlaskConfig.HOST, FlaskConfig.PORT, debug=FlaskConfig.DEBUG)
