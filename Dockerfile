FROM python:2.7
MAINTAINER Pasi Lammi <pasi.lammi@iki.fi>
ENV PYTHONUNBUFFERED 1

RUN apt-get update
RUN apt-get -y install python git
RUN mkdir -p /app /app/data
WORKDIR /app
RUN git clone https://github.com/dtcooper/python-fitparse.git
RUN pip install web.py Jinja2

RUN mv python-fitparse/fitparse /app
RUN rm -rf webpy python-fitparse
ADD web /app

ENTRYPOINT ["/usr/local/bin/python", "ui.py"]
EXPOSE 8080
VOLUME ["/app/data"]
