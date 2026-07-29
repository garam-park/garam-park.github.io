---
layout: post_with_ad
title: "Debian 11·12·13 Docker 설치: 검증·일반 사용자 권한·오류 해결"
date: 2024-02-10 04:43:47 +0900
last_modified_at: 2026-07-26 13:54:00 +0900
permalink: /docker/데비안(debian)에-도커(docker)-설치-하기
categories: docker
tags: docker install debian docker-engine
author: Garam Park
lang: ko
description: "Debian 11·12·13에서 Docker 공식 APT 저장소로 Engine과 Compose를 설치하고, 서비스·버전·hello-world 검증과 docker 그룹 권한 오류를 확인하는 방법입니다."
featured: true
---

> **Docker 공식 문서 기준 · 2026-07-26 업데이트**

Debian 11·12·13에서는 Docker 공식 APT 저장소를 등록한 뒤 Engine과 Compose를 설치하고, 서비스 상태·버전·`hello-world`를 차례로 확인하면 설치 성공 여부를 판정할 수 있습니다. `sudo` 없이 실행하는 설정은 선택 사항이며, 사용자를 `docker` 그룹에 추가하면 **root 수준 권한**을 부여하므로 다중 사용자 서버에서는 `sudo` 유지 또는 Rootless mode를 먼저 검토하세요.

이 글은 Docker 공식 APT 저장소로 새로 설치하는 환경을 대상으로 하며 다음 순서로 진행합니다.

1. 설치 전 조건 확인
2. Docker 공식 저장소 등록과 패키지 설치
3. 서비스·Engine·Compose·컨테이너 실행 검증
4. 일반 사용자 권한 설정
5. 설치 후 자주 만나는 오류 확인

## 1. 설치 전 조건 확인

Docker 공식 저장소 방식은 Debian 13(Trixie), 12(Bookworm), 11(Bullseye)을 지원합니다. 기존 Docker 패키지 충돌과 방화벽 주의사항은 [Debian Docker 설치 전 확인](/docker/debian-docker-설치-전-확인)에서 먼저 확인하세요.

아래 명령은 일반 사용자 기준입니다. root 셸에서 실행한다면 `sudo`를 빼면 됩니다.

## 2. Docker 공식 APT 저장소 등록

Docker의 GPG 키와 APT source를 등록합니다.

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

마지막 `apt update`가 오류 없이 끝나고 `download.docker.com` 저장소 정보가 표시되면 등록된 것입니다. Debian 파생 배포판에서는 `$VERSION_CODENAME` 대신 호환되는 Debian 안정판 코드명이 필요할 수 있습니다.

## 3. Docker Engine과 Compose 설치

Docker Engine, CLI, containerd, Buildx, Compose 플러그인을 함께 설치합니다.

```bash
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

## 4. 설치 직후 검증

### 4.1 Docker 서비스 상태

```bash
sudo systemctl status docker --no-pager
```

출력의 `Active:` 항목이 `active (running)`이면 데몬이 실행 중입니다. 실행 중이 아니라면 서비스를 시작하고 다시 확인합니다.

```bash
sudo systemctl start docker
sudo systemctl status docker --no-pager
```

### 4.2 Engine과 Compose 버전

```bash
docker --version
docker compose version
```

두 명령이 각각 `Docker version ...`과 `Docker Compose version ...`을 출력하면 CLI와 Compose 플러그인이 설치된 것입니다. 이 단계는 데몬 연결과 별개이므로 실제 컨테이너 실행도 확인해야 합니다.

### 4.3 hello-world 컨테이너 실행

일반 사용자 권한을 설정하기 전에는 `sudo`로 실행합니다.

```bash
sudo docker run hello-world
```

이미지를 내려받은 뒤 `Hello from Docker!`가 출력되고 컨테이너가 종료되면 Docker 데몬 연결, 이미지 다운로드, 컨테이너 실행까지 성공한 것입니다.

## 5. sudo 없이 Docker 실행하기

> **보안 주의:** `docker` 그룹 구성원은 Docker 데몬을 통해 호스트의 root 수준 권한을 얻을 수 있습니다. 권한 분리가 필요한 서버라면 그룹에 추가하지 말고 `sudo docker ...`를 유지하거나 [Docker Rootless mode](https://docs.docker.com/engine/security/rootless/)를 검토하세요.

패키지 설치 과정에서 `docker` 그룹이 이미 만들어질 수 있습니다. 그룹이 없을 때만 만든 뒤 현재 사용자를 추가합니다.

```bash
getent group docker || sudo groupadd docker
sudo usermod -aG docker "$USER"
```

로그아웃 후 다시 로그인하면 그룹 정보가 새로 적용됩니다. 현재 셸에서 바로 시험하려면 다음 명령으로 새 셸을 열 수 있습니다.

```bash
newgrp docker
```

`newgrp docker`의 효과는 그 셸에만 적용될 수 있습니다. 그룹 적용 여부와 `sudo` 없는 실행을 모두 확인합니다.

```bash
id -nG
docker run hello-world
```

`id -nG`에 `docker`가 포함되고 `Hello from Docker!`가 출력되면 적용된 것입니다. 권한 방식과 Rootless mode의 차이는 [sudo 없이 Docker 실행하기](/docker/sudo-없이-docker-실행하기)에서 더 자세히 확인할 수 있습니다.

## 6. 설치 후 오류 확인

### Cannot connect to the Docker daemon

`Cannot connect to the Docker daemon` 메시지는 먼저 데몬 실행 상태를 확인해야 한다는 뜻입니다.

```bash
sudo systemctl is-active docker
sudo systemctl start docker
sudo systemctl status docker --no-pager
```

`is-active` 결과가 `inactive` 또는 `failed`라면 시작 후 상태를 다시 확인하세요. 계속 실패하면 최근 서비스 로그에서 원인을 확인합니다.

```bash
sudo journalctl -u docker.service --no-pager -n 50
```

### permission denied while trying to connect to the Docker daemon socket

데몬은 실행 중인데 `/var/run/docker.sock` 권한 오류가 발생하면 현재 셸에 `docker` 그룹이 적용됐는지 확인합니다.

```bash
id -nG
ls -l /var/run/docker.sock
```

사용자가 `docker` 그룹에 없다면 앞 절의 `usermod`를 실행하고 로그아웃·로그인하세요. 그룹에 추가한 직후의 기존 셸이라면 `newgrp docker`로 새 셸에서 재검증할 수 있습니다. 소켓을 임의로 `chmod 666`으로 열어 권한 문제를 우회하지 마세요.

### ~/.docker/config.json permission denied

그룹 추가 전에 `sudo docker ...`를 실행해 `~/.docker`가 root 소유가 되면 다음과 같은 경고가 날 수 있습니다.

```text
WARNING: Error loading config file: /home/user/.docker/config.json: permission denied
```

Docker 공식 post-install 문서의 복구 방법대로 현재 사용자에게 소유권과 그룹 쓰기 권한을 돌려줍니다.

```bash
sudo chown "$USER":"$USER" "$HOME/.docker" -R
sudo chmod g+rwx "$HOME/.docker" -R
```

## 7. 최종 확인

다음 항목이 모두 맞으면 설치 후 검증이 끝난 것입니다.

- `systemctl status docker`가 `active (running)`을 표시합니다.
- `docker --version`과 `docker compose version`이 버전을 출력합니다.
- `sudo docker run hello-world`가 `Hello from Docker!`를 출력합니다.
- 일반 사용자 권한을 선택했다면 `id -nG`에 `docker`가 있고 `docker run hello-world`가 `sudo` 없이 성공합니다.
- 오류가 있으면 데몬 상태, 소켓 그룹 권한, `~/.docker` 소유권을 구분해 확인했습니다.

## 공식 문서와 관련 글

- [Docker 공식 Debian 설치 문서](https://docs.docker.com/engine/install/debian/)
- [Docker 공식 Linux 설치 후 설정](https://docs.docker.com/engine/install/linux-postinstall/)
- [Docker 공식 Rootless mode](https://docs.docker.com/engine/security/rootless/)
- [Debian Docker 설치 전 확인](/docker/debian-docker-설치-전-확인)
- [sudo 없이 Docker 실행하기](/docker/sudo-없이-docker-실행하기)
