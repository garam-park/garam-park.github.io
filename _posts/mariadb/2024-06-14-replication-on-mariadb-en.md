---
layout: post_with_ad
title: Setting up replication in MariaDB 11 version
date: 2024-06-14 11:04:51 +0900
permalink: /mariadb/2024-06-14-replication-on-mariadb
categories: mariadb
tags: mariadb, replication, slave, master
excerpt: Let's learn about MariaDB replication.
---

## What is MariaDB Replication?

MariaDB replication is the process of automatically transferring data changes that occur on a master database server to one or more slave database servers. This allows for maintaining duplicate copies of data, providing the following benefits:

- Data distribution and load balancing
- Data backup and recovery
- Failover and high availability
- Support for data warehousing and data mining analysis tasks

## Overview of the Replication Process

1. The master server records SQL statements in the binary log.
2. The I/O thread of the slave server reads the binary log events from the master and records them in the relay log.
3. The SQL thread of the slave executes the relay log events to replicate the data.

## Replication Setup Process

1. Master server configuration
    1. Enable binary logging
    2. Assign a unique server ID
2. Configure the master server information on the slave server
3. Start the replication process on the slave

After this, data changes on the master server are automatically replicated to the slave. You can monitor the replication status and perform failover if necessary.

---

### MariaDB Server Configuration

- server-id: Sets the unique identifier for the server. Used to identify each server when operating multiple servers.
- log_bin: Specifies the path to the binary log file. Used to log database changes and track the state of the database.
- expire_logs_days: Sets the number of days the binary log files are retained. Previous log files are automatically deleted after the specified number of days.
- max_binlog_size: Sets the maximum size of the binary log file. A new log file is created when the file size exceeds the specified size.

---

# Configuration

MariaDB 11 version does not have the `mysql` command, instead, it is executed with the `mariadb` command.

## 1. Master

### 1.1 Configuration

Configure `/etc/mysql/mariadb.conf.d/50-server.cnf`. It works as described for each setting above.

```bash
server-id              = 1
log_bin                = /var/log/mysql/mysql-bin.log
expire_logs_days       = 10
max_binlog_size        = 100M
```

<aside>
💡 Tested with server-id set to 0, but it did not work properly. server-id must start from 1

Fatal error: The slave I/O thread stops because master and slave have equal MariaDB server ids; these ids must be different for replication to work (or the --replicate-same-server-id option must be used on slave but this does not always make sense; please check the manual before using it).

</aside>

### 1.2 Create an account for the slave

Run `mariadb -u root -p` to create an account to be used on the slave.

```sql
grant replication slave on *.* to 'slave_db' @'%' identified by 'slave_password';
```

Restart MariaDB afterwards.

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

Save the File and Position values. The Position value will change every time there is a change in the master database.

# Slave

### 1.1 Configuration

Configure `/etc/mysql/mariadb.conf.d/50-server.cnf`.

```bash
server-id              = 2
```

<aside>
💡 The slave can operate even if only the `server-id` is set. If necessary, other options can also be specified.

</aside>

Restart MariaDB.

```bash
service mariadb restart # if necessary sudo
```

### 1.2 master 지정

Assume that the IP of the server where the master is running is 192.168.0.100 and the port is 3306.

Run `show master status;` and put the obtained value `FILE` as `MASTER_LOG_FILE`, `Position` as `MASTER_LOG_POS`.

```sql
CHANGE MASTER TO MASTER_HOST = "192.168.0.100",
MASTER_USER = "slave_db",
MASTER_PASSWORD = "slave_password",
MASTER_PORT = 3306,
MASTER_LOG_FILE = "mysql-bin.000002",
MASTER_LOG_POS = 342;
```

If it is applied correctly, start the slave.

```sql
start slave;
```

# Test

If you connect to the master and execute the following, you can confirm that it is applied the same way on the slave.

```sql
CREATE DATABASE foo;
USE foo;
CREATE TABLE users (name VARCHAR(255));
INSERT INTO users (name) VALUES ('홍길동');
INSERT INTO users (name) VALUES ('홍길순');
```