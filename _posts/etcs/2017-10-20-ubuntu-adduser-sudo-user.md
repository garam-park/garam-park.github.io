---
layout: post_with_ad
title: 우분투에서 sudo user 만들기
permalink: /linuxs/ubuntu-adduser-sudo-user
date:   2017-10-20 05:16:56 +0900
categories: linux adduser useradd
---

우분투 16.04 에서 root 뿐이 없는 상황에서 sudo 유저를 만드는 법을 정리해 보았다.

## **1. 유저 만들기** 

```shell
adduser username
```

위의 명령어는 'username' 라는 사용자를 만드는 명령어이다. 명령어를 실행하면 비밀번호(password)와 사용자의 정보를 입력하게 되어있다. 알맞게 작성하는 방법이외에 enter 를 눌러서 넘어갈 수 있다.

## **2.그룹에 추가**

```shell
adduser username sudo
```

username 를 sudo 그룹에 추가한다. sudo 그룹에 추가되면 sudo 명령어를 사용할 수 있게 된다.


```shell
apt install sudo
```

'sudo'  명령어가 없는 경우가 있는데, root 유저로 sudo 를 살치해 주어야 한다.