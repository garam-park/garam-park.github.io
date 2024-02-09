---
layout: post_with_ad
title: 데비안(debian)에 도커(docker) 설치 하기
date: 2024-02-10 04:43:47 +0900
permalink: /docker/데비안(debian)에-도커(docker)-설치-하기
categories: docker
tags: docker install
---

root 사용자로 진행한다는 전제입니다.

1. 데비안에 필요한 패키지 설치

```bash
apt-get update
```

```bash
apt-get install apt-transport-https ca-certificates curl gnupg2 software-properties-common -y
```

2 도커 GPG key 추가:

```bash
curl -fsSL https://download.docker.com/linux/debian/gpg | apt-key add -
```

1. 적절한 리포지토리 추가:

```bash
add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/debian $(lsb_release -cs) stable"
```

4. 다시 패키지 업데이트:

```bash
apt-get update
```

1. 도커 설치:

```bash
apt-get install docker-ce -y
```

1. 도커 버전 확인:

```bash
docker --version
```

이제 도커가 설치되었습니다. 간단한 컨테이너 실행을 통해 도커가 제대로 설치되었는지 확인할 수 있습니다.

```bash
docker run hello-world
```
