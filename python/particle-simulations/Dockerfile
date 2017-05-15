FROM natk/python-pythia

RUN apt-get install -y nginx python-pip
RUN service nginx stop

ADD nginx.conf /etc/nginx/
ADD supervisord.conf /etc/

RUN pip install gunicorn

RUN mkdir /var/www/particles
RUN mkdir /var/www/particles/logs

RUN pip install requests
RUN pip install flask
RUN pip install flask-cors
RUN pip install typing

RUN mkdir output

ADD data ./data
ADD util ./util
ADD api ./api

ADD run.py ./
ADD pythia_cfg.txt ./
ADD cfg.py ./
ADD wsgi.py ./

RUN pip2 install supervisor
RUN pip2 install supervisor-stdout

EXPOSE 8080

CMD supervisord -c /etc/supervisord.conf -n