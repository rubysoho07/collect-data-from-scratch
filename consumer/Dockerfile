FROM python:3.8-slim

WORKDIR /consumer

COPY requirements.txt /consumer

RUN pip install -r requirements.txt

COPY consumer.py /consumer

ENV PYTHONUNBUFFERED=1

CMD [ "python", "consumer.py" ]