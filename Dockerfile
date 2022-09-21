FROM python:3
ENV LANG C.UTF-8

RUN apt-get -y update && apt-get -y autoremove

RUN mkdir /app
WORKDIR /app

ADD requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

ADD . .

ENV DEBUG="False"

EXPOSE 8000
WORKDIR /app/fts-demo

CMD ["gunicorn", "fts-demo.wsgi", "--bind", "0.0.0.0:8000"]