from typing import Callable
from json import dumps as dump

from flask import Flask
from flask_cors import CORS

from cfg import *
from api import Response


class Server:
    def __init__(self,
                 ping_handler: Callable[[], Response]=None,
                 status_handler: Callable[[], Response]=None,
                 add_handler: Callable[[], Response]=None):
        self.app = Flask(__name__)
        CORS(self.app)

        # <editor-fold desc="Error Handlers">

        # noinspection PyUnusedLocal
        @self.app.errorhandler(403)
        def error403(e):
            return dump({"success": False, "error": 403, "message": "Sorry, you don't have permission to see that!"}), \
                   403

        # noinspection PyUnusedLocal
        @self.app.errorhandler(404)
        def error404(e):
            return dump({"success": False, "error": 404, "message": "Sorry, that path hasn't been implemented!"}), 404

        # noinspection PyUnusedLocal
        @self.app.errorhandler(500)
        def error500(e):
            return dump({"success": False, "error": 500, "message": "Sorry, there was an internal error!"}), 500

        # </editor-fold>

        if ping_handler is not None:
            @self.app.route('/')
            def ping() -> str:
                if ping_handler is not None:
                    return ping_handler().json

        if status_handler is not None:
            @self.app.route('/status')
            def status() -> str:
                return status_handler().json

        if add_handler is not None:
            @self.app.route('/add')
            def add() -> str:
                return add_handler().json

    def start_server(self, host=HOST, port=PORT):
        self.app.run(host, port)

if __name__ == '__main__':
    Server().start_server()
