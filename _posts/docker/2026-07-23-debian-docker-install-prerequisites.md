---
layout: post_with_ad
title: Debian에서 Docker 설치 전 확인: 지원 버전·패키지 충돌·방화벽
date: 2026-07-23 08:00:00 +0900
permalink: /docker/debian-docker-설치-전-확인
categories: docker
tags: docker debian firewall iptables
lang: ko
description: "Debian에서 Docker를 설치하기 전에 확인할 지원 버전, 기존 패키지 충돌, UFW·firewalld와 Docker 포트의 관계를 짧게 정리합니다."
---

> 빠른 설치 명령은 [Debian에 Docker 설치하기](/docker/데비안(debian)에-도커(docker)-설치-하기)에서 확인하세요.

## 1. 지원 Debian 버전

Docker 공식 APT 저장소 설치 방식은 현재 Debian **13(Trixie)**, **12(Bookworm)**, **11(Bullseye)**을 지원합니다. 테스트판·Kali 같은 파생 배포판은 현재 코드명이 아닌, 호환되는 Debian 안정판 코드명을 써야 할 수 있습니다.

## 2. 기존 Docker 패키지 충돌

`docker.io`, `docker-compose`, `containerd`, `runc` 등이 이미 설치되어 있으면 Docker 공식 패키지와 충돌할 수 있습니다. 기존 컨테이너·이미지·볼륨이 필요하면 먼저 백업 여부를 확인하세요.

```bash
sudo apt remove $(dpkg --get-selections docker.io docker-compose docker-doc podman-docker containerd runc | cut -f1)
```

새 서버라면 설치된 패키지가 없다는 메시지가 나와도 괜찮습니다.

## 3. 방화벽 주의

Docker로 포트를 공개하면 UFW나 firewalld 규칙을 우회할 수 있습니다. 인터넷에 공개하는 서버에서는 `docker run -p` 또는 Compose의 `ports`를 추가하기 전에 방화벽 정책을 먼저 확인하세요.

Docker는 `iptables-nft` 또는 `iptables-legacy`와 함께 사용해야 하며, Docker 컨테이너 트래픽에 별도 제한이 필요하면 `DOCKER-USER` 체인을 검토해야 합니다.

## 공식 문서

- [Docker 공식 Debian 설치 문서](https://docs.docker.com/engine/install/debian/)
- [Docker와 방화벽 안내](https://docs.docker.com/engine/network/packet-filtering-firewalls/)
