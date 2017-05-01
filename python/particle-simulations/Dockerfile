FROM natk/python-pythia

RUN pip install requests

ADD data ./data
ADD util ./util

ADD run.py ./
ADD cfg.txt ./

ENTRYPOINT python run.py