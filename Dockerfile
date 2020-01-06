FROM python:3.6-alpine

RUN adduser -D oaflopean
WORKDIR /home/copypasta
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

COPY requirements.txt requirements.txt
COPY static static
COPY migrations migrations
COPY templates templates
COPY app.py ./
COPY forms.py ./
COPY models.py ./
COPY boot.sh boot.sh

RUN chmod +x boot.sh
RUN chown -R oaflopean:oaflopean ./
RUN python3 -m venv venv
RUN venv/bin/pip3 install -r requirements.txt


ENV FLASK_APP app.py

EXPOSE 8000
RUN ./boot.sh
USER oaflopean
ENTRYPOINT ["gunicorn"  , "-b", "0.0.0.0:8000", "app:app"]

