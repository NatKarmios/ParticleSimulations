from datetime import datetime
from typing import Dict, Iterable

import requests
import json
import os

from data import DataFile

DEFAULT_DATA_DIR = "output/"
data_dir = DEFAULT_DATA_DIR


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
    with open(data_dir+"/"+filename, "a+") as file:
        file.write(",".join(map(str, data)) + "\n")


def upload_file_to_gists(files: Iterable[DataFile]) -> str:
    def read_files() -> Iterable[(str, Dict[str, str])]:
        for file in files:
            with open(data_dir + file.filename, "r") as f:
                yield (file.filename, {"content": f.read()})

    data = {
        "description": "Particle Collision Data | " + datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
        "public": True,
        "files": dict(read_files())
    }

    r = requests.post("https://api.github.com/gists", data=json.dumps(data))
    reply = json.loads(r.content.decode())
    return reply["html_url"]


def delete_file(filename: str) -> None:
    os.remove(data_dir+"/"+filename)
