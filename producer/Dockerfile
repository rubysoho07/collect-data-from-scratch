FROM python:3.8-slim

WORKDIR /producer

COPY requirements.txt api.py /producer/

RUN pip install -r requirements.txt 

EXPOSE 5000

CMD [ "gunicorn", "api:app", "-b", "0.0.0.0:5000" ]