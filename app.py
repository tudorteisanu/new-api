from src.app import app, FlaskConfig


if __name__ == '__main__':
    app.run(FlaskConfig.HOST, FlaskConfig.PORT, debug=FlaskConfig.DEBUG)
