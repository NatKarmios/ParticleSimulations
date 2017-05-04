from threading import Thread

from util import create_file, upload_file_to_gists

_pid = 0


class DataGetter:
    def __init__(self, type_):
        global _pid
        self.pid = _pid
        _pid += 1

        self.type = type_
        self.progress = 0
        self.started = False
        self.finished = False
        self.filename = None
        self.gist_url = None
        self._thread = Thread(target=self._thread_function)

    def start(self, with_thread=True):
        if with_thread:
            self._thread.start()
        else:
            self._thread.run()

    def _thread_function(self):
        self.filename = create_file(self.type)
        self.started = True
        
        self.get_data()

        upload_file_to_gists(self.filename)
        self.finished = True

    def get_data(self):
        raise NotImplementedError

    def __iter__(self):
        yield "pid", self.pid
        yield "started", self.started
        yield "finished", self.finished
        yield "progress", self.progress
        yield "gist_url", self.gist_url

    @property
    def dict(self):
        return dict(self)
