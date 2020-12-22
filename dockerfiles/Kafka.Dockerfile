FROM openjdk:8

WORKDIR /app

# Get Kafka
RUN wget https://downloads.apache.org/kafka/2.6.0/kafka_2.13-2.6.0.tgz && \
    tar -xzf kafka_2.13-2.6.0.tgz && \
    cd kafka_2.13-2.6.0

# Start the Kafka environment
RUN sed -i 's/zookeeper.connect=localhost:2181/zookeeper.connect=zoo1:2181,zoo2:2181,zoo3:2181/' config/server.properties

# 9092: Default server port for Kafka
EXPOSE 9092

# Kafka Broker Server Start
CMD [ "bin/kafka-server-start.sh", "config/server.properties" ]