FROM python:3.6-alpine



RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev


COPY requirements.txt requirements.txt

COPY . /app
WORKDIR /app

RUN pip install flask 
RUN pip install -r requirements.txt

ENTRYPOINT ["python"]
CMD ["app.py"]

