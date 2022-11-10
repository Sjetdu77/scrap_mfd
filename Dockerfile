FROM ubuntu:latest
RUN apt-get update -y && \
    apt-get install -y python3-pip python-is-python3

COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt
COPY . /app

CMD python ./main.py