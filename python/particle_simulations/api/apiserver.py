from typing import List, Dict, Callable

from data import Scatter
from data import Hist
from data import DataGetter

from api.server import Server
from api import Response


class APIServer:
    def __init__(self):
        self.server = Server(status_handler=self.__status,
                             add_handler=self.__add(),
                             del_handler=self.__del())

        self.started = False
        self.data_generators = []  # type: List[DataGetter]

    def __status(self) -> Response:
        return Response(data=self.get_status())

    def __add(self) -> Callable[[dict], Response]:
        def add(args: dict) -> Response:
            if not args:
                return Response(success=False, message="Your JSON was malformed!")

            try:
                if "params" in args:
                    params = args["params"]
                else:
                    params = {}

                if args["type"] == "scatter":
                    pid = self.add_scatter(params)
                elif args["type"] == "hist":
                    pid = self.add_hist(params)
                else:
                    raise ValueError
                return Response(message="Data generation successfully started!", data={"pid": pid})
            except (KeyError, ValueError):
                return Response(success=False, message="Invalid arguments!")
        return add

    def __del(self) -> Callable[[dict], Response]:
        def del_(args: dict) -> Response:
            if not args:
                return Response(success=False, message="Your JSON was malformed!")

            try:
                self.delete_generator(args["pid"])
                return Response(message="Generator successfully deleted.", data={"pid": args["pid"]})
            except IndexError:
                return Response(success=False, message="That generator doesn't exist!")
            except (KeyError, ValueError):
                return Response(success=False, message="Invalid arguments!")
        return del_

    def get_status(self) -> Dict[str, List]:
        return {"generators": list(map(lambda generator: generator.dict, self.data_generators))}

    def add_scatter(self, params: dict) -> int:
        scatter = Scatter(**params)
        self.data_generators.append(scatter)
        scatter.start()
        return scatter.pid

    def add_hist(self, params: dict) -> int:
        hist = Hist(**params)
        self.data_generators.append(hist)
        hist.start()
        return hist.pid

    def delete_generator(self, pid: int):
        self.data_generators.pop(pid).cancel()

    def get_flask(self):
        self.started = True
        return self.server.app
