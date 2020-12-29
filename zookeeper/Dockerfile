FROM openjdk:11-slim

WORKDIR /zookeeper

# Get Zookeeper
RUN apt-get update -qq && apt-get install wget -y -qq && \
    wget --quiet https://downloads.apache.org/zookeeper/zookeeper-3.6.2/apache-zookeeper-3.6.2-bin.tar.gz && \
    tar -zxf apache-zookeeper-3.6.2-bin.tar.gz && \
    cd apache-zookeeper-3.6.2-bin

# 2181: Port for client
# 2888: Port for follower
# 3888: Port for election
EXPOSE 2181 2888 3888

# Make directory for storing data
RUN mkdir -p /data

# Copy Zookeeper configuration file
COPY *.cfg /zookeeper/apache-zookeeper-3.6.2-bin/conf/

# Copy script file to run ZooKeeper.
COPY run-zookeeper.sh .

# Start Zookeeper Server
CMD [ "./run-zookeeper.sh" ]