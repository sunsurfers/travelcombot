FROM python:slim

WORKDIR /usr/src/app

ADD requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

ADD . .
ADD apt install gcc

CMD python main.py
