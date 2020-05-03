"""
This script runs the wechatAutoReplay application using a development server.
"""

from os import environ
from wechatAutoReplay import app
import logging

if __name__ == '__main__':
    HOST = environ.get('SERVER_HOST', 'localhost')
    try:
       PORT = int(environ.get('SERVER_PORT', '8080'))
    except ValueError:
        PORT = 8080

    # app.debug = True
    handler = logging.FileHandler('flask.log',encoding='UTF-8')
    handler.setLevel(logging.DEBUG)
    logging_format = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')
    handler.setFormatter(logging_format)
    app.logger.addHandler(handler)
    app.run(HOST, PORT)
