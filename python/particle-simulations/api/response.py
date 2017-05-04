from json import dumps


class Response:
    def __init__(self, message: str=None, success: bool=True, data: dict=None):
        self.__success = success  # type: bool
        self.__message = message  # type: str
        self.__data = data  # type: dict

    @property
    def success(self) -> bool:
        return self.__success

    @property
    def message(self) -> str:
        return self.__message

    @property
    def data(self) -> dict:
        return self.__data

    @property
    def json(self) -> str:
        return dumps(dict(self))

    def __iter__(self):
        yield "success", self.success
        if self.message is not None:
            yield "message", self.message
        if self.data is not None:
            yield "data", self.data
