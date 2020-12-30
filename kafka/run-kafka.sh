#!/bin/sh

cd kafka_2.13-2.6.0

# Set log file directory
sed -i 's/log.dirs=\/tmp\/kafka-logs/log.dirs=\/data/' config/server.properties

if [ -n "${STANDALONE_MODE}" ]; then
    # Set ZooKeeper connection
    sed -i 's/zookeeper.connect=localhost:2181/zookeeper.connect=zookeeper:2181/' config/server.properties
else
    HOST_ID=$(hostname | cut -d - -f 2)
    # Set Broker ID
    sed -i 's/broker.id=0/broker.id='${HOST_ID}'/' config/server.properties

    # Set ZooKeeper connection
    sed -i 's/zookeeper.connect=localhost:2181/zookeeper.connect=zookeeper-0.zookeeper.default.svc.cluster.local:2181,zookeeper-1.zookeeper.default.svc.cluster.local:2181,zookeeper-2.zookeeper.default.svc.cluster.local:2181/' config/server.properties
fi

# Remove unnecessary files of /data (Log file directory)
rm -rf /data

bin/kafka-server-start.sh config/server.properties