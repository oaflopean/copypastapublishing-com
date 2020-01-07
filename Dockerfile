FROM python:3.6-alpine

RUN adduser -D oaflopean

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev
USER oaflopean

COPY requirements.txt requirements.txt
COPY static static
COPY migrations migrations
COPY templates templates
COPY app.py ./
COPY forms.py ./
COPY models.py ./



RUN chown -R oaflopean:oaflopean ./
RUN pip install -r requirements.txt
RUN pip install flask gunicorn

ENV FLASK_APP app.py

EXPOSE 8000

ENTRYPOINT ["gunicorn"  , "-b", "0.0.0.0:8000", "app"]

