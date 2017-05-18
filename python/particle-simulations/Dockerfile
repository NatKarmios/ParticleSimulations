FROM natk/python-pythia

RUN pip install gunicorn requests flask flask-cors typing

RUN mkdir output

ADD data ./data
ADD util ./util
ADD api ./api

ADD run.py ./
ADD pythia_cfg.txt ./
ADD cfg.py ./
ADD wsgi.py ./

EXPOSE 5000

CMD gunicorn wsgi:app -b 0.0.0.0:5000 --log-level=debug