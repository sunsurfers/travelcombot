FROM python:slim

WORKDIR /usr/src/app
ADD apt install gcc
ADD requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

ADD . .


CMD python main.py
