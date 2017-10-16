FROM python:3
MAINTAINER Dan Marner <dands@marner.org>
EXPOSE 5000

RUN mkdir /app
WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY . /app

CMD python anawd.py