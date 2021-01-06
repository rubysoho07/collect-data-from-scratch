FROM python:3.8-slim

WORKDIR /producer

COPY requirements.txt /producer

RUN pip install -r requirements.txt 

COPY api.py /producer

ENV PYTHONUNBUFFERED=1

EXPOSE 5000

CMD [ "gunicorn", "api:app", "-b", "0.0.0.0:5000" ]