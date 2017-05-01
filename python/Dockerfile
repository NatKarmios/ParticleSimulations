FROM natk/python-pythia

RUN pip install requests
RUN pip install json

ADD data ./data
ADD util ./util

ADD run.py ./
ADD cfg.txt ./

ENTRYPOINT python run.py