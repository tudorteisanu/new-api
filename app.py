from application import create_app, FlaskConfig

app = create_app()

if __name__ == '__main__':
    app.run(FlaskConfig.HOST, FlaskConfig.PORT, FlaskConfig.DEBUG)
