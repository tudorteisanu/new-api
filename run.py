from settings import app
from config import configType as Config
from flask import jsonify
from helpers.validation import validate
from helpers.common import create_dirs, save_logs_to_file

import urls

@app.before_request
def before_request():
    try:
        errors = validate()
    
        if len(errors):
            return jsonify({'message': "Invalid data", "errors": errors}), 422
    except:
        pass

from helpers.send_standart_message import send_test_message

app.route('/test')(send_test_message)

create_dirs()
save_logs_to_file()


if __name__ == '__main__':
    app.run(Config.HOST, Config.PORT, Config.DEBUG)



