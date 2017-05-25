
from api import APIServer

api_server = APIServer()  # type: APIServer
app = api_server.get_flask()
