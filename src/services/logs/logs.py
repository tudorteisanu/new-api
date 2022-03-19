import logging


def init_logging(app):
    log_format_str = '[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s'
    logging.basicConfig(format=log_format_str, filename="logs/global.log", level=logging.DEBUG)
    formatter = logging.Formatter(log_format_str, '%m-%d %H:%M:%S')
    file_handler = logging.FileHandler("logs/summary.log")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logging.getLogger('sqlalchemy.engine').setLevel(logging.DEBUG)
    logging.getLogger('sqlalchemy.dialects').setLevel(logging.DEBUG)
    logging.getLogger('sqlalchemy.pool').setLevel(logging.DEBUG)
    logging.getLogger('sqlalchemy.orm').setLevel(logging.DEBUG)
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    stream_handler.setFormatter(formatter)
    app.logger.addHandler(file_handler)
    app.logger.addHandler(stream_handler)
    app.logger.info("Logging is set up.")

