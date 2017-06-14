from threading import Thread
from typing import Tuple, Dict

from util import create_file, upload_file_to_gists, delete_file, write_line_to_file

_pid = 0


class DataFile:
    def __init__(self, filename_prefix: str, headers: Tuple[str, ...]):
        self.filename_prefix = filename_prefix
        self.filename = create_file(filename_prefix + "_")

        self.headers = headers
        if self.headers is not None:
            self.write(headers)

    def write(self, data):
        write_line_to_file(self.filename, data)

    def delete(self):
        delete_file(self.filename)


class DataGetter:
    def __init__(self, files: Dict[str, Tuple[str, ...]]):
        global _pid
        self.pid = _pid
        _pid += 1

        self.file_scheme = files  # type: Dict[str, Tuple[str, ...]]
        self.progress = 0  # type: float
        self.finished = False  # type: bool
        self.files = None  # type: Dict[str, DataFile]
        self.gist_url = None  # type: str
        self.cancelled = False
        self._thread = Thread(target=self._thread_function)

    def start(self, with_thread=True):
        if with_thread:
            self._thread.start()
        else:
            self._thread.run()

    def _thread_function(self):
        self.files = dict((name, DataFile(name, headers) for name, headers in self.file_scheme.items()))

        self.get_data()
        if self.cancelled:
            [f.delete() for f in self.files.values()]
            print("{} cancelled.".format(self.pid))
        else:
            self.gist_url = upload_file_to_gists(self.files.values())
            self.progress = 1.0
            self.finished = True
            print("{} finished.".format(self.pid))

    def get_data(self):
        raise NotImplementedError

    def _update(self, progress: float=None) -> None:
        if progress is not None:
            self.progress = progress

    def __iter__(self):
        yield "pid", self.pid
        yield "files", self.files
        yield "finished", self.finished
        yield "progress", self.progress
        yield "gist_url", self.gist_url

    @property
    def dict(self):
        return dict(self)

    def cancel(self):
        self.cancelled = True
