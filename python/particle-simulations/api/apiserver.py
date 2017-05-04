from typing import List, Dict

from data import Scatter
from data import DataGetter

from api.server import Server
from api import Response


class APIServer:
    def __init__(self):
        self.server = Server(ping_handler=lambda: Response(message="Hello there!"),
                             status_handler=self.__status,
                             add_handler=self.__add)

        self.started = False
        self.data_generators = []  # type: List[DataGetter]

    def __status(self) -> Response:
        return Response(data=self.get_status())

    def __add(self, args: dict) -> Response:
        try:
            if args["type"] == "scatter":
                self.add_scatter(**args["params"])
            else:
                raise ValueError
            return Response(message="Data generation successfully started!")
        except (KeyError, ValueError):
            return Response(success=False, message="Invalid arguments!")

    def start(self):
        self.server.start_server()
        self.started = True

    def get_status(self) -> Dict[str, List]:
        return {"generators": list(map(lambda generator: generator.dict, self.data_generators))}

    def add_scatter(self, **params):
        scatter = Scatter(energy_step=params["energy_step"], events_per_energy_step=params["events_per_energy_step"])
        self.data_generators.append(scatter)
        scatter.start()


if __name__ == '__main__':
    api = APIServer()
    api.start()
