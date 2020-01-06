FROM python:3.6-alpine

RUN adduser -D oaflopean

WORKDIR /home/

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn

COPY static static
COPY app.py ./
RUN chmod +x boot.sh

ENV FLASK_APP app.py

RUN chown -R app:app ./
USER oaflopean

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]