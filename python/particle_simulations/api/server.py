from json import dumps as dump
from typing import Callable, Dict

from flask import Flask, request
from flask import Response as FlaskResponse
from flask_cors import CORS

from api import Response
from api.auth import Auth


class Server:
    def __init__(self,
                 ping_handler: Callable[[], Response]=lambda: Response(message="Hello there!"),
                 status_handler: Callable[[], Response]=None,
                 add_handler: Callable[[Dict], Response]=None,
                 del_handler: Callable[[Dict], Response]=None):

        self.app = Flask(__name__)
        CORS(self.app)

        self.auth = Auth()

        # <editor-fold desc="Error Handlers">

        # noinspection PyUnusedLocal
        @self.app.errorhandler(403)
        def error403(e):
            return dump({"success": False, "error": 403, "message": "Sorry, you don't have permission to do that!"}), \
                   403

        # noinspection PyUnusedLocal
        @self.app.errorhandler(404)
        def error404(e):
            return dump({"success": False, "error": 404, "message": "Sorry, that path doesn't exist!"}), 404

        # noinspection PyUnusedLocal
        @self.app.errorhandler(500)
        def error500(e):
            return dump({"success": False, "error": 500, "message": "Sorry, there was an internal error!"}), 500

        # </editor-fold>

        @self.app.route('/')
        def ping() -> FlaskResponse:
            return ping_handler().reply

        if status_handler is not None:
            @self.app.route('/status')
            def status() -> FlaskResponse:
                return status_handler().reply

        if add_handler is not None:
            @self.app.route('/add', methods=['POST'])
            @self.auth.requires_auth
            def add() -> FlaskResponse:
                return add_handler(request.json).reply

        if del_handler is not None:
            @self.app.route('/del', methods=['POST'])
            @self.auth.requires_auth
            def del_() -> FlaskResponse:
                return del_handler(request.json).reply

        @self.app.route('/login', methods=['POST'])
        def login() -> FlaskResponse:
            return self.auth.login(request.json)

        @self.app.route('/test_auth')
        @self.auth.requires_auth
        def test_auth() -> FlaskResponse:
            return ping_handler().reply
