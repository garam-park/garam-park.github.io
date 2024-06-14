---
layout: post_with_ad
title: mariadb 11 version replication set 설정하기
date: 2024-06-14 11:04:51 +0900
permalink: /mariadb/2024-06-14-replication-on-mariadb
categories: mariadb
tags: mariadb, replication, slave, master
excerpt: MariaDB Replication에 대해 알아보겠습니다.
---

## MariaDB 복제(Replication)란?

MariaDB 복제는 하나의 마스터 데이터베이스 서버에서 발생한 데이터 변경 내용을 다른 하나 이상의 슬레이브 데이터베이스 서버로 자동으로 전송하는 프로세스를 말합니다. 이를 통해 데이터의 중복 복사본을 유지할 수 있어 다음과 같은 이점이 있습니다.

- 데이터 분산 및 로드 밸런싱
- 데이터 백업 및 복구
- 장애 조치 및 고가용성 제공
- 데이터 웨어하우징 및 데이터 마이닝 등의 분석 작업 지원

## 복제 프로세스 개요

1. 마스터 서버에서 바이너리 로그에 SQL 문을 기록합니다.
2. 슬레이브 서버의 I/O 스레드가 마스터의 바이너리 로그 이벤트를 읽어 릴레이 로그에 기록합니다.
3. 슬레이브의 SQL 스레드가 릴레이 로그 이벤트를 실행하여 데이터를 복제합니다.[2]

## 복제 설정 과정

1. 마스터 서버 설정
    1. 바이너리 로깅을 활성화
    2. 고유한 서버 ID를 지정
2. 슬레이브 서버에서 마스터 서버 정보를 설정
3. 슬레이브에서 복제 프로세스를 시작

이후 마스터 서버의 데이터 변경 내용이 슬레이브로 자동 복제됩니다. 복제 상태를 모니터링하고 필요한 경우 장애 조치를 수행할 수 있습니다.

---

### mariadb server config 설정

- server-id: 서버의 고유 식별자를 설정합니다. 여러 서버를 운영할 때 각 서버를 식별하는 데 사용됩니다.
- log_bin: 이진 로그 파일의 경로를 지정합니다. 데이터베이스 변경 사항을 로깅하여 데이터베이스의 상태를 추적하는 데 사용됩니다.
- expire_logs_days: 이진 로그 파일이 유지되는 일 수를 설정합니다. 지정된 일 수 이후에는 이전 로그 파일이 자동으로 삭제됩니다.
- max_binlog_size: 이진 로그 파일의 최대 크기를 설정합니다. 파일 크기가 지정된 크기를 초과하면 새로운 로그 파일이 생성됩니다.

---

# 설정 하기

mariadb 11 버전은 이전 버전과 다르게 `mysql` 명령어가 없고 대신 `mariadb` 명령어로 실행됩니다. 

## 1. Master

### 1.1 configuraiton

`/etc/mysql/mariadb.conf.d/50-server.cnf` 설정합니다. 위에서 각 설정에 대해서 설명한 것과 같이 동작합니다.

```bash
server-id              = 1
log_bin                = /var/log/mysql/mysql-bin.log
expire_logs_days       = 10
max_binlog_size        = 100M
```

<aside>
💡 server-id 를 0으로 해서 테스트 해보았는데 정상 작동 불가. server-id 는 1부터 시작

Fatal error: The slave I/O thread stops because master and slave have equal MariaDB server ids; these ids must be different for replication to work (or the --replicate-same-server-id option must be used on slave but this does not always make sense; please check the manual before using it).

</aside>

### 1.2 slave 를 위한 계정 생성

`mariadb -u root -p` 실행하여 slave 에서 사용할 계정을 생성합니다.

```sql
grant replication slave on *.* to 'slave_db' @'%' identified by 'slave_password';
```

이후에 maridb 를 restart 합니다.

```bash
service mariadb restart #필요시 sudo
```

### **1.3 binay log 확인**

```sql
show master status;
```

```bash
MariaDB [(none)]> show master status;
```

```bash
+------------------+----------+--------------+------------------+
| File             | Position | Binlog_Do_DB | Binlog_Ignore_DB |
+------------------+----------+--------------+------------------+
| mysql-bin.000002 |      342 |              |                  |
+------------------+----------+--------------+------------------+
1 row in set (0.000 sec)
```

위에서 File 과 Position 값을 저장해 둡니다. master 데이터베이스에 변경 사항이 있을 때마다 Postion 값이 달라집니다.

# Slave

### 1.1 configuraiton

`/etc/mysql/mariadb.conf.d/50-server.cnf` 설정합니다. 

```bash
server-id              = 2
```

<aside>
💡 slave 에서는 `server-id` 만 설정해도 동작합니다. 필요시 다른 옵션도 지정합니다.

</aside>

mariadb 를 재시작합니다.

```bash
service mariadb restart #필요시 sudo
```

### 1.2 master 지정

마스터가 동작하는 server 의 ip 가 192.168.0.100 이고 port 가 3306 이라고 가정합니다. 마스터에서 

`show master status;` 를 실행하고 얻은 값 `FILE` 은 `MASTER_LOG_FILE`, `Position` 은 `MASTER_LOG_POS` 으로 넣어줍니다.

```sql
CHANGE MASTER TO MASTER_HOST = "192.168.0.100",
MASTER_USER = "slave_db",
MASTER_PASSWORD = "slave_password",
MASTER_PORT = 3306,
MASTER_LOG_FILE = "mysql-bin.000002",
MASTER_LOG_POS = 342;
```

잘 적용이 되었으면 slave 를 실행합니다.

```sql
start slave;
```

# 테스트해보기

master에서 접속하고 다음과 같이 실행하면 slave 에서도 동일하게 적용된 것을 확인할 수 있습니다.

```sql
CREATE DATABASE foo;
USE foo;
CREATE TABLE users (name VARCHAR(255));
INSERT INTO users (name) VALUES ('홍길동');
INSERT INTO users (name) VALUES ('홍길순');
```