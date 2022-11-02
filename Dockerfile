FROM python:3.10.6

COPY . /FlaskBugTracker
WORKDIR /FlaskBugTracker

RUN pip3 install -r requirements.txt

CMD gunicorn -c gunicorn.conf.py app:app --preload
