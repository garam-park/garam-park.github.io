---
layout: post_with_ad
title:  우분투에  MariaDB 설치하기
date:   2018-09-27 22:02:48 +0900
permalink : /mariadb/install-mariadb-on-unbuntu
categories: database, db, mariadb
tags : install, mariadb
excerpt : 마리아디비를 우분투에 설치해보자
lang: ko
description: "우분투에 MariaDB를 설치하는 방법. apt로 서버를 설치하고 보안 초기 설정까지 진행하는 과정을 정리합니다."
---

## 설치

```shell
sudo apt install mariadb-server
```

## 보안 처리

```shell
sudo mysql_secure_installation
```

## 외부에 연결할 수 있도록 처리


