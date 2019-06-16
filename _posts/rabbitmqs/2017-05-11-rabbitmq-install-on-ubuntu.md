---
layout: post_with_ad
title:  우분투에 RabbtiMQ 설치
date:   2018-05-11 06:36:51 +0900
permalink : /rabbitmqs/rabbitmq-install-on-ubuntu
categories: rabbitmq, ubuntu
tags : rabbitmq, ubuntu
excerpt : 우분투에 RabbtiMQ 설치하기
---
# 우분투에 RabbtiMQ 설치하기

이 포스트는 RabbitMQ 를 Bintray Apt 레파지토리를 통해서 설치하는 방법에 대해서 다룬다. RabbitMQ를 사용하기 위해서는 Erlang 이 설치되어 있어야한다. 우분투에 Erlang 설치는 [여기](/rabbitmqs/erlang-install-on-linux)를 확인하자.

설치하려는 RabbitMQ 버전을 확인하여 지원하는 Erlang 을 설치해야한다. 현재(2018년 5월)에는 3.7 RabbitMQ 가 최신이고 이 버전에는 Erlang 19.3 ~ 20.3버전을 사용할 수 있다. 자세한 내용은 [여기](http://www.rabbitmq.com/which-erlang.html)를 확인하자.

source list directory(/etc/apt/sources.list.d)에 APT 레파지토리를 추가하기 위해서는 아래의 실행문에 {distribution} 부분을 수정 후 실행하자.

```shell
echo "deb https://dl.bintray.com/rabbitmq/debian {distribution} main" | sudo tee /etc/apt/sources.list.d/bintray.rabbitmq.list
```
distribution 부분에는 코드네임을 넣으면 된다. 아래를 실행하면 코드네임을 알 수 있다.

```shell
lsb_release --codename
```

16.04의 경우 `xenial` 이고 다음과 같이 실행하면 된다.

```shell
echo "deb https://dl.bintray.com/rabbitmq/debian xenial main" | sudo tee /etc/apt/sources.list.d/bintray.rabbitmq.list
```
지원되는 distributions 리스트는 아래외 같다.

- artful
- jessie
- precise
- sid
- stretch
- trusty
- wheezy
- xenial
- yakkety
- zesty

다음은 trudsted key 리스트에 RabbitMq 의 공개키를 추가해준다. bintray 를 사용하는 방법과 rabbitmq에서 직접 제공하는 것을 받는 방법 2가지가 있다.

**bintray 에서 제공 :**

```shell
wget -O- https://dl.bintray.com/rabbitmq/Keys/rabbitmq-release-signing-key.asc |
     sudo apt-key add -
```

**rabbitmq 에서 제공 :**

```shell
wget -O- https://www.rabbitmq.com/rabbitmq-release-signing-key.asc | sudo apt-key add -
```

업데이트를 실행하고

```shell
sudo apt-get update
Install rabbitmq-server package:
```

RabbitMQ를 설치하자.

```shell
sudo apt-get install rabbitmq-server
```

실행하는 방법은 아래와 같다.

```shell
service rabbitmq-server start
```
