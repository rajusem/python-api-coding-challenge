FROM python:3-alpine

MAINTAINER Raj Zalavadia

COPY . /app

WORKDIR /app

RUN pip3 install -r requirements.txt

CMD ["gunicorn" ,"--workers=3", "-b", "0.0.0.0:5000", "run:app"]