import os
import json
import logging

from datetime import datetime
from random import randint

from flask import Flask
from flask import request

from kafka import KafkaProducer

app = Flask(__name__)

# Logger Configuration
logger = logging.getLogger("KAFKA_PRODUCER")
logger.setLevel(logging.INFO)

handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s [%(name)s] [%(levelname)s] %(message)s')

handler.setFormatter(formatter)
logger.addHandler(handler)


# Connect to Kafka Producer
if 'STANDALONE_MODE' in os.environ.keys():
    bootstrap_servers = "kafka:9092"
else:
    bootstrap_servers = [
        "kafka-0.kafka.default.svc.cluster.local:9092",
        "kafka-1.kafka.default.svc.cluster.local:9092",
        "kafka-2.kafka.default.svc.cluster.local:9092" 
    ]

producer = KafkaProducer(bootstrap_servers=bootstrap_servers)
logger.info("Connected to Kafka")

@app.route('/upload', methods=['POST'])
def upload():

    if request.method == 'POST':
        

        message = {
            "message": f"Random Message: {randint(1, 1000)}",
            "username": f"user-{randint(1, 1000):04d}",
            "eventTime": datetime.now().isoformat(timespec="milliseconds")
        }

        logger.info(f"Message prepared: {message['message']}")
        producer.send("test-topic", json.dumps(message, ensure_ascii=False).encode())
        logger.info(f"Sent message to Kafka: {message['message']}")

        return message
    else:
        return "Not Available"
