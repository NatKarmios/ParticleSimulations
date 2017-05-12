import random
import string
from functools import wraps
from flask import request

from api.response import Response

from cfg import PASSWD

TOKEN_SIZE = 10


class Auth:
    def __init__(self):
        self.tokens = []

    def _gen_token(self) -> str:
        token = None
        while token is None or token in self.tokens:
            token = \
                ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(TOKEN_SIZE))
        self.tokens.append(token)
        return token

    def login(self, args):
        if not args:
            return Response("Your JSON was malformed!", False).reply
        try:
            if args["pass"] == PASSWD:
                return Response("Successfully authenticated.", True, {"token": self._gen_token()}).reply
            else:
                return self.authenticate()
        except KeyError:
            return Response("Invalid arguments!", False).reply

    def check_auth(self, _, token):
        """This function is called to check if a username /
        password combination is valid.
        """
        return token in self.tokens

    @staticmethod
    def authenticate():
        return Response("Invalid authentication!", False).reply

    def requires_auth(self, f):
        @wraps(f)
        def decorated(*args, **kwargs):
            auth = request.authorization
            if not auth or not self.check_auth(auth.username, auth.password):
                return self.authenticate()
            return f(*args, **kwargs)

        return decorated
