from config.settings import app
from config.flask_config import FlaskConfig
from config.settings import login_manager
from modules.users.models import User
from flask import render_template
from flask_jwt_extended import decode_token
from datetime import datetime
from flask_login import logout_user


@login_manager.request_loader
def load_user_from_request(request):
    if request.headers.get('Authorization', None):
        token = decode_token(request.headers.get('Authorization'))
        token_expiry = datetime.fromtimestamp(token['exp'])

        if token_expiry < datetime.now():
            logout_user()
            return {"message": "token_expire"}
        return User.query.get(token['identity'])
    return None


@app.route('/login')
def login():
    return render_template('login.html')


if __name__ == '__main__':
    import urls

    app.run(FlaskConfig.HOST, FlaskConfig.PORT, FlaskConfig.DEBUG)
