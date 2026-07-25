---
layout: post_with_ad
title: sudo 없이 Docker 실행하기: docker 그룹 권한 설정
date: 2024-02-10 04:22:57 +0900
permalink: /docker/sudo-없이-docker-실행하기
categories: docker
tags: docker sudo rootless permissions
lang: ko
description: "Docker를 sudo 없이 실행하도록 docker 그룹에 사용자를 추가하는 방법과 root 수준 권한 주의사항을 정리합니다."
---

> Docker 설치가 먼저 필요하다면 [Debian에 Docker 설치하기](/docker/데비안(debian)에-도커(docker)-설치-하기)를 확인하세요.

기본 Docker 소켓은 root가 소유합니다. `sudo docker ...` 대신 현재 사용자가 실행하려면 아래 명령을 사용합니다.

```bash
sudo groupadd docker
sudo usermod -aG docker $USER
newgrp docker
```

새 셸에서 동작을 확인합니다.

```bash
docker run hello-world
```

`groupadd: group 'docker' already exists`가 나오면 이미 만들어진 그룹이므로 다음 명령으로 진행하면 됩니다.

> **주의:** `docker` 그룹은 root 수준 권한을 부여합니다. 다중 사용자 서버나 권한 분리가 필요한 환경에서는 무조건 그룹에 추가하지 말고, `sudo docker ...`를 유지하거나 Rootless mode를 검토하세요.

Rootless mode는 Docker 데몬 자체를 비-root 사용자로 실행하는 별도 방식입니다. `docker` 그룹에 사용자를 추가하는 것과는 다릅니다.

- [Docker 공식 설치 후 설정](https://docs.docker.com/engine/install/linux-postinstall/)
- [Docker 공식 Rootless mode](https://docs.docker.com/engine/security/rootless/)
