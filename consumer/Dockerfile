FROM python:3.8-slim

WORKDIR /consumer

COPY requirements.txt consumer.py /consumer/

RUN pip install -r requirements.txt

ENV PYTHONUNBUFFERED=1

CMD [ "python", "consumer.py" ]