from settings import app
from config import configType as Config

from common.common import create_dirs, save_logs_to_file

from urls import *

@app.before_request
def before_request_func():
    pass


create_dirs()
save_logs_to_file()

if __name__ == '__main__':
    app.run(Config.HOST, Config.PORT, Config.DEBUG)
