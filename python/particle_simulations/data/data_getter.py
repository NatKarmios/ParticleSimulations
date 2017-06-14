from threading import Thread
from typing import Tuple, Dict

from util import upload_files_to_gists, DataFile

_pid = 0


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
        self.files = dict()
        for name, headers in self.file_scheme.items():
            self.files[name] = DataFile(name, headers)

        self.get_data()
        if self.cancelled:
            [f.delete() for f in self.files.values()]
            print("{} cancelled.".format(self.pid))
        else:
            self.gist_url = upload_files_to_gists(self.files.values())
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
        yield "files", self.files_dict
        yield "finished", self.finished
        yield "progress", self.progress
        yield "gist_url", self.gist_url

    @property
    def dict(self):
        return dict(self)

    @property
    def files_dict(self):
        files = dict()
        for filename, data in self.files.items():
            files[filename] = data.dict
        return files

    def cancel(self):
        self.cancelled = True
