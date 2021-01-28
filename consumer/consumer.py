import os
import uuid
import logging

import boto3

from kafka import KafkaConsumer

BUCKET_NAME = os.environ.get('S3_BUCKET_NAME')
MAX_RECORDS_TO_STORE = 10


# Logger Configuration
logger = logging.getLogger("KAFKA_CONSUMER")
logger.setLevel(logging.INFO)

handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s [%(name)s] [%(levelname)s] %(message)s')

handler.setFormatter(formatter)
logger.addHandler(handler)



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
    
    return KafkaConsumer(bootstrap_servers=bootstrap_servers, group_id='test-topic-group')


def store_data(s3_client, body: bytes) -> dict:

    response = s3_client.put_object(
        Bucket=BUCKET_NAME, Key=str(uuid.uuid4()),
        Body=body
    )

    return response


if __name__ == "__main__":

    s3 = get_s3_client()

    bucket_name = os.environ.get('S3_BUCKET_NAME')

    if bucket_name is None:
        raise ValueError('Bucket name is None')

    consumer = get_kafka_consumer()
    logger.info("Connected to Kafka")

    consumer.subscribe(['test-topic'])

    count = 0
    data = []

    while True:
        messages = consumer.poll(timeout_ms=30000)

        # Example of 'messages'
        """
        {
            TopicPartition(topic='test-topic', partition=0): [
                ConsumerRecord(topic='test-topic', partition=0, offset=21, timestamp=1611839857976, 
                timestamp_type=0, key=None, 
                value=b'{"message": "Random Message: 420", "username": "user-0377", "eventTime": "2021-01-28T13:17:37.976"}', 
                headers=[], checksum=None, serialized_key_size=-1, serialized_value_size=99, serialized_header_size=-1)
            ]
        }
        """

        if len(messages) == 0 and count > 0:
            logger.info("Storing remained data...")
            response = store_data(s3, b'\n'.join(data))
            logger.info(response)

            count = 0
            data.clear()

        for topic_partition in messages:
            for consumer_record in messages[topic_partition]:
                data.append(consumer_record.value)
                count += 1

                if count >= MAX_RECORDS_TO_STORE:
                    response = store_data(s3, b'\n'.join(data))
                    logger.info(response)

                    count = 0
                    data.clear()

