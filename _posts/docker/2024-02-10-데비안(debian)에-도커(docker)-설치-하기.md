---
layout: post_with_ad
title: 데비안(debian)에 도커(docker) 설치 하기
date: 2024-02-10 04:43:47 +0900
last_modified_at: 2026-07-23 10:16:00 +0900
permalink: /docker/데비안(debian)에-도커(docker)-설치-하기
categories: docker
tags: docker install debian docker-engine
author: Garam Park
lang: ko
description: "Debian 11·12·13에서 Docker 공식 APT 저장소로 Docker Engine과 Compose를 설치하고 확인하는 빠른 방법입니다."
featured: true
image: /images/featured/docker.svg
---

> **Docker 공식 방법 기준 · 2026-07-23 업데이트**
> - 설치 전 확인: [Debian 지원 버전·패키지 충돌·방화벽 주의사항](/docker/debian-docker-설치-전-확인)
> - `sudo` 없이 실행: [Docker 그룹 권한과 Rootless mode](/docker/sudo-없이-docker-실행하기)
> - 원문: [Docker 공식 Debian 설치 문서](https://docs.docker.com/engine/install/debian/)

아래 명령은 일반 사용자 기준입니다. root로 실행한다면 `sudo`를 빼면 됩니다.

## 1. Docker 공식 저장소 등록

```bash
sudo apt update
sudo apt install -y ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/debian/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

sudo tee /etc/apt/sources.list.d/docker.sources <<EOF
Types: deb
URIs: https://download.docker.com/linux/debian
Suites: $(. /etc/os-release && echo "$VERSION_CODENAME")
Components: stable
Architectures: $(dpkg --print-architecture)
Signed-By: /etc/apt/keyrings/docker.asc
EOF

sudo apt update
```

## 2. Docker와 Compose 설치

```bash
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

## 3. 설치 확인

```bash
sudo docker run hello-world
docker --version
docker compose version
```

`Hello from Docker!`가 출력되면 설치가 완료된 것입니다.

> `sudo` 없이 Docker를 실행해야 한다면 [Docker 그룹 권한과 Rootless mode](/docker/sudo-없이-docker-실행하기)를 먼저 확인하세요.
