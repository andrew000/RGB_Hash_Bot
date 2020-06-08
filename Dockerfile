FROM python:3.7-slim

RUN python3 -m pip install --upgrade pip

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY main.py /bin
COPY core /bin/core

CMD python3 /bin/main.py
