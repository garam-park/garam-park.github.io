---
layout: post_with_ad
title:  Erlang(얼랭) 우분투에 설치하기
date: 2018-05-09 21:59:27 +0900
permalink : /rabbitmqs/erlang-install-on-linux
categories: rabbitmq, erlang
tags :  erlang, install, ubuntu, erlang install, erlang ubuntu, erlang install on ubuntu
excerpt : Erlang 을 우분투에 설치하려면...
---
# **우분투에 Erlang 설치하기**

## 1. 레파지토리 엔드리 추가하기

얼랭 솔루션 레파지토리를 받기위해서는 다음 코드를 실행한다. 아래의 코드는 apt-secure 를 위한 public key도 포함 되어있다.

```sh
wget https://packages.erlang-solutions.com/erlang-solutions_1.0_all.deb
sudo dpkg -i erlang-solutions_1.0_all.deb
```

## 2.  Erlang 설치하기
레파지토리 캐시를 리프레시하고, Erlang 패키지를 설치한다.

```sh
sudo apt-get update
sudo apt-get install erlang
```

아니며  "esl-erlang" 패키지를 설치한다.

```sh
sudo apt-get update
sudo apt-get install esl-erlang
```
