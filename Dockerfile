FROM python:3.6-alpine

RUN adduser -D oaflopean


COPY requirements.txt requirements.txt
COPY static static

RUN python static/psycopg2/setup.py build
RUN python setup.py install

RUN python -m venv venv

RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn

COPY app.py ./
RUN chmod +x boot.sh

ENV FLASK_APP app.py

RUN chown -R app:app ./
USER oaflopean

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]