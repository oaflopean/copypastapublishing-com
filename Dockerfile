FROM python:3.6-alpine



RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev


COPY requirements.txt requirements.txt
COPY static static
COPY migrations migrations
COPY templates templates
COPY app.py app.py
COPY forms.py forms.py
COPY models.py models.py

RUN pip install -r requirements.txt
RUN pip install flask gunicorn

ENV FLASK_APP app.py

EXPOSE 8000

ENTRYPOINT ["gunicorn"  , "-b", "0.0.0.0:8000", "app:cp-web"]

