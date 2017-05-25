from threading import Thread
from typing import Iterable

from util import create_file, upload_file_to_gists, delete_file, write_line_to_file

_pid = 0


class DataGetter:
    def __init__(self, type_: str, headers: Iterable[str]):
        global _pid
        self.pid = _pid
        _pid += 1

        self.type = type_  # type: str
        self.headers = headers
        self.progress = 0  # type: float
        self.finished = False  # type: bool
        self.filename = None  # type: str
        self.gist_url = None  # type: str
        self.cancelled = False
        self._thread = Thread(target=self._thread_function)

    def start(self, with_thread=True):
        if with_thread:
            self._thread.start()
        else:
            self._thread.run()

    def _thread_function(self):
        self.filename = create_file(self.type+"_")
        self.write(self.headers)
        
        self.get_data()
        if self.cancelled:
            delete_file(self.filename)
            print("{} cancelled.".format(self.pid))
        else:
            self.gist_url = upload_file_to_gists(self.filename)
            self.progress = 1.0
            self.finished = True
            print("{} finished.".format(self.pid))

    def get_data(self):
        raise NotImplementedError

    def _update(self, progress: float=None) -> None:
        if progress is not None:
            self.progress = progress

    def write(self, data):
        write_line_to_file(self.filename, data)

    def __iter__(self):
        yield "pid", self.pid
        yield "type", self.type
        yield "finished", self.finished
        yield "progress", self.progress
        yield "gist_url", self.gist_url

    @property
    def dict(self):
        return dict(self)

    def cancel(self):
        self.cancelled = True
