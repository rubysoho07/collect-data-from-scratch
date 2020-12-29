#!/bin/sh

cd apache-zookeeper-3.6.2-bin/

if [ -n "${STANDALONE_MODE}" ]; then
    cd conf/
    rm zoo.cfg
    mv zoo.standalone.cfg zoo.cfg
    cd ..
else
    HOST_ID=$(hostname | cut -d - -f 2)
    expr $HOST_ID + 1 > /data/myid
fi

bin/zkServer.sh start-foreground