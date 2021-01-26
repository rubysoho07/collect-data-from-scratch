import os
import json

from datetime import datetime
from random import randint

from flask import Flask
from flask import request

from kafka import KafkaProducer

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload():

    if request.method == 'POST':
        if 'STANDALONE_MODE' in os.environ.keys():
            bootstrap_servers = "kafka:9092"
        else:
            bootstrap_servers = [
                "kafka-0.kafka.default.svc.cluster.local:9092",
                "kafka-1.kafka.default.svc.cluster.local:9092",
                "kafka-2.kafka.default.svc.cluster.local:9092" 
            ]
        
        producer = KafkaProducer(bootstrap_servers=bootstrap_servers)

        message = {
            "message": f"Random Message: {randint(1, 1000)}",
            "username": f"user-{randint(1, 1000):04d}",
            "eventTime": datetime.now().isoformat(timespec="milliseconds")
        }

        producer.send("test-topic", json.dumps(message, ensure_ascii=False).encode())

        return message
    else:
        return "Not Available"
