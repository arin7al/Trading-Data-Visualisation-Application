FROM python:3

FROM ubuntu:latest
MAINTAINER Selvyn Wright "swright@celestial.co.uk"
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD [ "./webtier.py" ]