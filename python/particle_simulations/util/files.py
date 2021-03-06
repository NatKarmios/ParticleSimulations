from datetime import datetime
from pprint import pformat
from typing import Dict, Iterable, Tuple

import requests
import json
import os

DEFAULT_DATA_DIR = "output/"
data_dir = DEFAULT_DATA_DIR


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

    def __iter__(self):
        yield "filename_prefix", self.filename_prefix
        yield "filename", self.filename
        yield "headers", self.headers

    @property
    def dict(self):
        return dict(self)


def _create_data_dir(dir_name=data_dir):
    global data_dir
    data_dir = dir_name

    if not os.path.isdir(data_dir):
        os.mkdir(data_dir)


def create_file(prefix="") -> str:
    from datetime import datetime
    filename = prefix + "particle-data_" + datetime.utcnow().strftime("%Y-%m-%dT%H-%M-%S" + ".csv")
    open(data_dir+filename, "w+").close()
    return filename


def write_line_to_file(filename, data) -> None:
    if "".join(map(str, data)) != "":
        with open(data_dir+"/"+filename, "a+") as file:
            file.write(",".join(map(str, data)) + ("," if len(tuple(data)) == 1 else "") + "\n")


def upload_files_to_gists(files: Iterable[DataFile]) -> str:
    def read_files() -> Dict[str, Dict[str, str]]:
        files_dict = dict()
        for file in files:
            with open(data_dir + file.filename, "r") as f:
                content = f.read()
            if content.replace("\n", "") != "":
                files_dict[file.filename] = {"content": content}
        return files_dict

    data = {
        "description": "Particle Collision Data | " + datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
        "public": True,
        "files": read_files()
    }

    r = requests.post("https://api.github.com/gists", data=json.dumps(data))
    reply = json.loads(r.content.decode())
    try:
        return reply["html_url"]
    except KeyError:
        raise Exception(pformat(reply, indent=2))


def delete_file(filename: str) -> None:
    os.remove(data_dir+"/"+filename)
