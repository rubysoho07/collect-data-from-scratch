# Collect Data From Scratch

데이터 수집 및 저장을 위한 시스템을 밑바닥부터 만들어보는 과정을 기록합니다.

클라우드 서비스 공급자의 매니지드 서비스에 상관없이, Kubernetes를 통해 어떤 환경에도 배포할 수 있도록 하는 것을 목표로 합니다.

## Docker 이미지 빌드

### ZooKeeper 이미지 빌드

```shell script
cd zookeeper/
docker login
docker build -t cdfs-zookeeper . 
docker tag cdfs-zookeeper [Docker Hub ID]/cdfs-zookeeper:latest
docker push [Docker Hub ID]/cdfs-zookeeper:latest
```
### Kafka 이미지 빌드

```shell script
cd kafka/
docker login
docker build -t cdfs-kafka .
docker tag cdfs-kafka [Docker Hub ID]/cdfs-kafka:latest
docker push [Docker Hub ID]/cdfs-kafka:latest
```
## 로컬에서 테스트하기

컨테이너 간 통신을 위해 [User-defined Bridge Network](https://docs.docker.com/network/network-tutorial-standalone/)를 이용합니다. 

아래 명령으로 ZooKeeper와 Kafka 컨테이너를 올립니다. 

```shell script
docker network create --driver bridge cdfs-network
docker run -d -e STANDALONE_MODE=yes --network cdfs-network --name zookeeper cdfs-zookeeper
docker run -d -e STANDALONE_MODE=yes --network cdfs-network --name kafka cdfs-kafka
```

그러면 먼저 Topic을 만들고, 이벤트를 한 번 보내 봅시다. ([Kafka Quickstart을 참조했습니다.](https://kafka.apache.org/quickstart))

```shell script
docker exec -it kafka bash
root@02c750bdca04:/kafka# cd kafka_2.13-2.6.0
root@02c750bdca04:/kafka/kafka_2.13-2.6.0# bin/kafka-topics.sh --create --topic quickstart-events --bootstrap-server localhost:9092
Created topic quickstart-events.
root@02c750bdca04:/kafka/kafka_2.13-2.6.0# bin/kafka-console-producer.sh --topic quickstart-events --bootstrap-server localhost:9092
>first
>second
```

다른 터미널 창에서 다음과 같이 입력해서 이벤트를 읽어봅시다. 

```shell script
docker exec -it kafka bash
root@02c750bdca04:/kafka# cd kafka_2.13-2.6.0
root@02c750bdca04:/kafka/kafka_2.13-2.6.0# bin/kafka-console-consumer.sh --topic quickstart-events --from-beginning --bootstrap-server localhost:9092
first
second
```

종료하려면 Ctrl+C를 누른 뒤, exit 명령을 입력합니다.

### 정리하기

```shell script
docker stop zookeeper kafka
docker rm zookeeper kafka
docker network rm cdfs-network
```

## Kubernetes로 배포하기

모든 설명은 minikube, kubectl이 설치되어 있음을 기준으로 합니다.

### minikube 시작하기

```shell script
minikube start
```

### ZooKeeper 배포하기

```shell script
cd k8s_config
kubectl apply -f zookeeper-service.yaml
```

#### 정상 작동 확인하기

먼저 ZooKeeper가 동작 중인 Pod에 데이터를 써 봅니다.

```shell script
kubectl exec zookeeper-0 -i -t -- bash
cd apache-zookeeper-3.6.2-bin/bin
source zkCli.sh create /hello world
```

아래와 같이 나오면 성공입니다.

```
WATCHER::

WatchedEvent state:SyncConnected type:None path:null
Created /hello
2020-12-29 09:03:50,997 [myid:] - ERROR [main:ServiceUtils@42] - Exiting JVM with code 0
```

그리고 ZooKeeper가 동작 중인 다른 Pod에서 다음 명령을 실행합니다.

```shell script
kubectl exec zookeeper-1 -i -t -- bash
cd apache-zookeeper-3.6.2-bin/bin
./zkCli.sh get /hello
```

아래와 같이 나오면 성공입니다.

```
WATCHER::

WatchedEvent state:SyncConnected type:None path:null
world
2020-12-29 09:05:42,849 [myid:] - ERROR [main:ServiceUtils@42] - Exiting JVM with code 0
```

### Kakfa 배포하기

```shell script
cd k8s_config
kubectl apply -f kafka-service.yaml
```

#### 정상 작동 확인하기

* (참고) 아래에서 설명하는 내용은 minikube에서 돌리기에 부족할 수 있습니다. 참고로 보시기를 권장하며, 실제로 테스트 하시려면 Kubernetes 클러스터를 올려서 테스트 해 보시기 바랍니다. (비용이 부과될 수 있음)

먼저 Kafka Pod 중 하나를 선택해서 Topic을 만들고, Producer 역할로서 메시지를 보내 봅니다.

```shell script
kubectl exec -it kafka-0 -- bash
root@kafka-0:/kafka# cd kafka_2.13-2.6.0
root@kafka-0:/kafka/kafka_2.13-2.6.0# bin/kafka-topics.sh --create --topic quickstart-events --bootstrap-server `hostname -f`:9092 --replication-factor 3 --partitions 20
Created topic quickstart-events.
root@kafka-0:/kafka/kafka_2.13-2.6.0# bin/kafka-console-producer.sh --topic quickstart-events --bootstrap-server `hostname -f`:9092
>message 1
>message 2
```

그리고 다른 터미널을 실행해서, 다른 Kafka Pod에서 Consumer 역할을 수행해 봅니다. 

```shell script
kubectl exec -it kafka-1 -- bash
root@kafka-1:/kafka# cd kafka_2.13-2.6.0
root@kafka-1:/kafka/kafka_2.13-2.6.0# bin/kafka-console-consumer.sh --topic quickstart-events --from-beginning --bootstrap-server `hostname -f`:9092
message 1
message 2
```

위 결과에서 확인할 수 있듯이, 메시지를 잘 받고 있네요.
## 참고자료

### Kubernetes 문서

* [서비스](https://kubernetes.io/ko/docs/concepts/services-networking/service/)
* [스테이트풀셋(StatefulSet)](https://kubernetes.io/ko/docs/concepts/workloads/controllers/statefulset/)
* [분산 시스템 코디네이터 ZooKeeper 실행하기](https://kubernetes.io/ko/docs/tutorials/stateful-application/zookeeper/)
* [초기화 컨테이너(Init Containers) 디버그하기](https://kubernetes.io/ko/docs/tasks/debug-application-cluster/debug-init-containers/)
