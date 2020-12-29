# Collect Data From Scratch

데이터 수집 및 저장을 위한 시스템을 밑바닥부터 만들어보는 과정을 기록합니다.

클라우드 서비스 공급자의 매니지드 서비스에 상관없이, Kubernetes를 통해 어떤 환경에도 배포할 수 있도록 하는 것을 목표로 합니다.

## Docker 이미지 빌드

### ZooKeeper 이미지 빌드

```shell script
cd zookeeper/
docker login
docker build -t cdfs-zookeeper . 
docker tag -t cdfs-zookeeper [Docker Hub ID]/cdfs-zookeeper:latest
docker push [Docker Hub ID]/cdfs-zookeeper:latest
```
### Kafka 이미지 빌드


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

## 참고자료

### Kubernetes 문서

* [서비스](https://kubernetes.io/ko/docs/concepts/services-networking/service/)
* [스테이트풀셋(StatefulSet)](https://kubernetes.io/ko/docs/concepts/workloads/controllers/statefulset/)
* [분산 시스템 코디네이터 ZooKeeper 실행하기](https://kubernetes.io/ko/docs/tutorials/stateful-application/zookeeper/)
* [초기화 컨테이너(Init Containers) 디버그하기](https://kubernetes.io/ko/docs/tasks/debug-application-cluster/debug-init-containers/)
