FROM openjdk:8

WORKDIR /zookeeper

# Get Zookeeper
RUN wget https://downloads.apache.org/zookeeper/zookeeper-3.6.2/apache-zookeeper-3.6.2-bin.tar.gz && \
    tar -xfz apache-zookeeper-3.6.2-bin.tar.gz && \
    cd apache-zookeeper-3.6.2-bin

# 2181: Port for client
# 2888: Port for follower
# 3888: Port for election
EXPOSE 2181 2888 3888

# Make directory for storing data
RUN mkdir -p /data

# Copy Zookeeper configuration file
COPY zookeeper.cfg /zookeeper/conf/

# Write /data/myid file (Default: 1)
RUN echo ${ZOOKEEPER_ID:-1} > /data/myid

# Start Zookeeper Server
CMD [ "bin/zkServer.sh", "start-foreground" ]