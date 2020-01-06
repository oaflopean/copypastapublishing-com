FROM python:3.6-alpine

RUN adduser -D oaflopean
USER oaflopean
WORKDIR /home/copypasta
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

COPY requirements.txt requirements.txt
COPY static static
RUN python -m venv venv

RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn

COPY app.py ./
COPY boot.sh boot.sh
RUN chmod +x boot.sh

ENV FLASK_APP app.py

RUN chown -R oaflopean:oaflopean ./
WORKDIR /home/copypasta
RUN ./boot.sh
EXPOSE 8000
ENTRYPOINT ["gunicorn"  , "-b", "0.0.0.0:8000", "app:app"]

