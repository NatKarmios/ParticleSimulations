from threading import Thread

from util import create_file, upload_file_to_gists

_pid = 0


class DataGetter:
    def __init__(self, type_: str):
        global _pid
        self.pid = _pid
        _pid += 1

        self.type = type_  # type: str
        self.progress = 0  # type: float
        self.started = False  # type: bool
        self.finished = False  # type: bool
        self.filename = None  # type: str
        self.gist_url = None  # type: str
        self._thread = Thread(target=self._thread_function)

    def start(self, with_thread=True):
        if with_thread:
            self._thread.start()
        else:
            self._thread.run()

    def _thread_function(self):
        self.filename = create_file("_"+self.type)
        self.started = True
        
        self.get_data()

        self.gist_url = upload_file_to_gists(self.filename)
        self.progress = 1.0
        self.finished = True
        print("{} finished.".format(self.pid))

    def get_data(self):
        raise NotImplementedError

    def _update(self, progress: float=None, message: str=None):
        if progress is not None:
            self.progress = progress
        print("{}: {:.2%}{}".format(self.pid, self.progress, "" if message is None else " [{}]".format(message)))

    def __iter__(self):
        yield "pid", self.pid
        yield "started", self.started
        yield "finished", self.finished
        yield "progress", self.progress
        yield "gist_url", self.gist_url

    @property
    def dict(self):
        return dict(self)
