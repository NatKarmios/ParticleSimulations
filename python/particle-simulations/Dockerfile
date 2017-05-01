FROM natk/python-pythia

RUN pip install requests

RUN mkdir output

ADD data ./data
ADD util ./util

ADD run.py ./
ADD cfg.txt ./

ENTRYPOINT python run.py