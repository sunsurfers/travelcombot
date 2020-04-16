FROM python:slim

WORKDIR /usr/src/app

RUN apt update && apt install -y --no-install-recommends gcc

ADD requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

ADD . .

CMD python main.py
