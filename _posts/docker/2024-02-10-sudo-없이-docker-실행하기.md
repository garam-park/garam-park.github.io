---
layout: post_with_ad
title: sudo 없이 docker 실행하기
date: 2024-02-10 04:22:57 +0900
permalink: /docker/sudo-없이-docker-실행하기
categories: docker
tags: docker sudo
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
