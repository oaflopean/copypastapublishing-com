FROM python:3.6-alpine


COPY . /

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev 
RUN pip install -r requirements.txt


EXPOSE 5000
ENTRYPOINT ["gunicorn","-b","0.0.0.0:5000", "app:application"]

