FROM natk/python-pythia

RUN pip install requests
RUN pip install flask
RUN pip install flask-cors
RUN pip install typing

RUN mkdir output

ADD data ./data
ADD util ./util
ADD api ./api

ADD run.py ./
ADD cfg.txt ./
ADD cfg.py ./

EXPOSE 8080

ENTRYPOINT python run.py