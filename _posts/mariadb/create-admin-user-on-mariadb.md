---
layout: post_with_ad
title:  MariaDB에 Admin 계정을 만들어보자
date:   2018-09-27 22:31:35 +0900
permalink : /mariadb/create-admin-user-on-mariadb
categories: database, db, mariadb
tags : create user, mariadb, admin
excerpt : root 유저 말고 다른 유저로 어드민 권한을 주고 싶을때 어떻게 해야할까?
---

MariaDB를 설치하고 나서 root 말고 맞춤형으로

### 새로운 유저 생성 방법

아래의 예제는 ***storyg*** 라는 유저를 생성하고 접속하는 것은 자신의 환경인 ***localhost*** 애서만 접속할 수 있도록 했다. 암호는 ***password***로 지정했다.

```sql
CREATE USER 'storyg'@'localhost' IDENTIFIED BY 'password';
```

아래의 예제는 ***sasha*** 라는 유저를 생성하고 접속하는 것은 자신의 환경인 ***172.16.0.10*** 애서만 접속할 수 있도록 했다. 암호는 ***secret***로 지정했다.

```sql
CREATE USER 'sasha'@'172.16.0.4' IDENTIFIED BY 'secret';
```

### 