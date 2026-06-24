---
layout: post_with_ad
title: sudo 없이 docker 실행하기
date: 2024-02-10 04:22:57 +0900
permalink: /docker/sudo-없이-docker-실행하기
categories: docker
tags: docker sudo
lang: ko
description: "Docker 명령을 sudo 없이 실행하는 방법. docker 그룹을 만들고 사용자를 추가해 권한을 부여하는 절차를 정리합니다."
---

### 도커그룹생성

```yaml
sudo groupadd docker
```

### 도커그룹에 유저추가

```yaml
sudo usermod -aG docker ${USER}
```

or

```yaml
sudo gpasswd -a $USER docker
```

### 도커 재시작

```yaml
sudo service docker restart
```

### `현재 사용자 로그아웃 및 재로그인 필수`

`exit` 하고 `su username` 하던 재접속 필수

### 테스트

```yaml
docker ps
```
