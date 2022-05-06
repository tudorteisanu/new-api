from src.app import app, FlaskConfig


if __name__ == '__main__':
    from werkzeug.middleware.profiler import ProfilerMiddleware
    app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[5], profile_dir='./profile')

    app.run(FlaskConfig.HOST, FlaskConfig.PORT, debug=FlaskConfig.DEBUG)
