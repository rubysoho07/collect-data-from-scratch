import os
import uuid

import boto3

from kafka import KafkaConsumer

def _validate_env(value):
    """ Validation of environment variable. If valid, return True """

    if value in ["", None, "undefined", "null", "None"]:
        return False

    return True


def get_s3_client():
    """ Get S3 Client from config """

    if 'S3_ENDPOINT' in os.environ.keys() and _validate_env(os.environ.get('S3_ENDPOINT')) is True:
        # For S3 Compatible Storage
        client = boto3.client('s3', endpoint_url=os.environ.get('S3_ENDPOINT'))
    else:
        client = boto3.client('s3')
    
    return client

def get_kafka_consumer():
    """ Get Kafka Consumer """

    if 'STANDALONE_MODE' in os.environ.keys():
        bootstrap_servers = "kafka:9092"
    else:
        bootstrap_servers = [
                "kafka-0.kafka.default.svc.cluster.local:9092",
                "kafka-1.kafka.default.svc.cluster.local:9092",
                "kafka-2.kafka.default.svc.cluster.local:9092" 
            ]
    
    return KafkaConsumer(bootstrap_servers=bootstrap_servers)

if __name__ == "__main__":

    s3 = get_s3_client()

    bucket_name = os.environ.get('S3_BUCKET_NAME')

    if bucket_name is None:
        raise ValueError('Bucket name is None')

    consumer = get_kafka_consumer()

    consumer.subscribe(['test-topic'])

    count = 0
    data = b''

    for msg in consumer:
        data = data + msg.value + b'\n'
        count = count + 1

        if count >= 10:
            response = s3.put_object(
                Bucket=bucket_name, 
                Key=str(uuid.uuid4()),
                Body=data
            )

            print(response)
            count = 0
            data = b''

