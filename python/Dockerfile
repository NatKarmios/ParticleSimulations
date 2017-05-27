FROM natk/python-pythia

RUN pip install gunicorn

RUN pip install requests
RUN pip install flask
RUN pip install flask-cors
RUN pip install typing

RUN mkdir output

ADD ./particle_simulations/data ./data
ADD ./particle_simulations/util ./util
ADD ./particle_simulations/api ./api

ADD ./particle_simulations/wsgi.py ./

VOLUME ./cfg


EXPOSE 5000

CMD gunicorn wsgi:app -b 0.0.0.0:5000 --log-level=debug