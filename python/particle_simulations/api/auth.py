import random
import string
from functools import wraps
from typing import Callable

from flask import request

from api.response import Response

try:
    from cfg.cfg import *
except ImportError:
    raise FileNotFoundError("cfg.py not found!")

TOKEN_SIZE = 10


class Auth:
    def __init__(self):
        self.tokens = []  # type: list

    def _gen_token(self) -> str:
        token = None  # type: str
        while token is None or token in self.tokens:
            token = \
                ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(TOKEN_SIZE))
        self.tokens.append(token)
        return token

    def login(self, args: dict) -> Response:
        if not args:
            return Response("Your JSON was malformed!", False).reply
        try:
            if args["pass"] == PASSWD:
                return Response("Successfully authenticated.", True, {"token": self._gen_token()}).reply
            else:
                return self.auth_failed()
        except KeyError:
            return Response("Invalid arguments!", False).reply

    def check_auth(self, token: str) -> bool:
        return token in self.tokens

    @staticmethod
    def auth_failed():
        return Response("Invalid authentication!", False).reply

    def requires_auth(self, f: Callable) -> Callable:
        @wraps(f)
        def decorated(*args, **kwargs):
            auth = request.authorization
            if not auth or not self.check_auth(auth.password):
                return self.auth_failed()
            return f(*args, **kwargs)

        return decorated
