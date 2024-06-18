---
layout: post_with_ad
title: 우분투 도커 설치 (root user 용)
date: 2024-06-18 11:04:51 +0900
permalink: /20240618/kr/install-docker-on-ubuntu-for-root
categories: web api
tags: docker, ubuntu
excerpt: (root 용)우분투에 도커를 설치하는 방법을 알아봅시다.
---

## **목차**

* 우분투 시스템 패키지 업데이트
* 필요한 패키지 설치
* Docker의 공식 GPG키를 추가
* Docker의 공식 리포지토리를 추가
* 업데이트 및 도커 설치
* 도커 상태 확인
* 도커 시작
* 도커 실행
* 도커 자동 시작

### 한번에 실행하기

급하신분은 여기서 그냥 실행 시키시면 됩니다.

#### 설치하기

```sh
apt-get update && \
apt-get install -y apt-transport-https ca-certificates curl gnupg-agent software-properties-common && \
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add - && \
add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" && \
apt-get update && \
apt-get install -y docker-ce docker-ce-cli containerd.io
```

### docker 부팅시 자동 실행
```sh
systemctl status docker
systemctl start docker # 필요시
systemctl enable docker
```

### 우분투 시스템 패키지 업데이트

우분투 시스템의 패키지를 최신 상태로 업데이트합니다.

```sh
apt-get update
```

### 필요한 패키지 설치

필요한 패키지를 설치합니다

```sh
apt-get install apt-transport-https ca-certificates curl gnupg-agent software-properties-common
```

### Docker의 공식 GPG키를 추가

Docker의 공식 GPG 키를 다운로드하고 apt-key에 추가합니다.

```sh
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -
```

### Docker의 공식 리포지토리를 추가

Docker의 공식 리포지토리를 추가합니다.

```sh
add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
```

### 업데이트 및 도커 설치

업데이트 및 도커를 설치합니다.

```sh
apt-get update
```

### 도커 설치


Docker CE (Community Edition), Docker CE CLI (Command Line Interface), 그리고 containerd.io를 설치합니다.

```sh
apt-get install docker-ce docker-ce-cli containerd.io
```

### 도커 상태 확인

도커가 정상 설치되었는지 확인합니다.

```sh
systemctl status docker
```

### 도커 시작

도커가 꺼져있다면 켜주세요.

```sh
systemctl start docker
```

### 도커 테스트 실행

테스트로 도커를 실행합니다. 

```sh
docker run hello-world
```

설치가 정상적으로 되었다면 다음과 같은 메세지가 나옵니다.

```
Hello from Docker!
This message shows that your installation appears to be working correctly.

To generate this message, Docker took the following steps:
 1. The Docker client contacted the Docker daemon.
 2. The Docker daemon pulled the "hello-world" image from the Docker Hub.
    (arm64v8)
 3. The Docker daemon created a new container from that image which runs the
    executable that produces the output you are currently reading.
 4. The Docker daemon streamed that output to the Docker client, which sent it
    to your terminal.

To try something more ambitious, you can run an Ubuntu container with:
 $ docker run -it ubuntu bash

Share images, automate workflows, and more with a free Docker ID:
 https://hub.docker.com/

For more examples and ideas, visit:
 https://docs.docker.com/get-started/
 ```


### 도커 자동 시작

부팅시 도커를 자동 시작하도록 설정합니다.

```sh
systemctl enable docker
```


