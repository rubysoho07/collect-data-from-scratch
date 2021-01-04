FROM python:3.8-slim

WORKDIR /producer

COPY requirements.txt api.py /producer/

RUN pip install -r requirements.txt 

EXPOSE 5000

ENV FLASK_APP=api.py

CMD [ "flask", "run", "--host=0.0.0.0" ]