---
layout     : post_with_ad
title      : 우분투에서 외부 접속을 좀 더 안전하게 하기(우분투 ssh 접속 보안 설정)
date       : 2018-04-21 01:16:53 +0900
permalink  : /linuxs/ubuntu-setup-security
categories : ubuntu linux
tags       : ssh sshd secure root 접근제한 암호제한
excerpt    : 우분투에서 외부 접속을 좀 더 안전하게 하기
---
# **1 소개**

우분투 서버를 관리하고 있는데 우분투의 외부접속을 좀더 제한하여 보안을 강화해보기로 했습니다. 보안 강화는 접속 제한 두 가지를 두고 SSH 키 자체에 암호를 거는 것. 이렇게 세 가지를 통합니다.

## **2 사용자 생성**

우선은 sudo 권한이 있는 계정으로 서버로 접속합니다. 저는 example.com 도메인이 등록된 서버에 접속을 한다고 가정하고 서술합니다.

```shell
ssh root@example.com
```

위의 명령어처럼 해서 서버에 접속합니다. 이후에 아래의 명령어와 같이 하여 사용자를 추가합니다. 아래는 사용자 username이 'storyg'이 유저를 추가하는 명령어입니다.

```shell
adduser storyg
```

명령어를 실행하면 이름, 비밀번호 등을 입력하도록 지문이 나오게 됩니다. 적당한 값을 입력해주세요. 사용자가 추가되면 sudo 권한을 갖도록 해줍니다. sudo 권한을 주지 않으려먼 주지 않아도 무방합니다.

```bash
adduser storyg sudo
```

생성된 user 'storyg'로 su(switch user) 해보겠습니다.

```bash
su strogy
```

adduser 명령어에서 입력한 비밀번호를 입력하면 유저를 변경할 수 있습니다. 'storyg' 유저에서 빠저나오도록 'exit' 명령어를 입력합니다.

```bash
exit
```

서버에서 빠저나오도록 root 유저에서 한번 더 빠저 나옵니다.

```bash
exit
```

원격에서 storyg 계정으로 접속합니다.

```bash
ssh storyg@example.com
```

sshd_config 파일에서 루트 로그인하지 못하도록 설정하겠습니다. 우선은 sshd_config 파일을 열어줍니다.

```bash
sudo vim /etc/ssh/sshd_config
```

`PermitRootLogin` 설정이 yes 로 되어있습니다.

```shell
#...
PermitRootLogin yes
#...
/PermitRootLogin
```

yes 를 no로 변경해 주고 저장하고 종료합니다.

```shell
#...
PermitRootLogin no
#...
:wq
```

설정을 적용하려면 다시 시작해야합니다.

```shell
sudo service sshd restart
# ubuntu 16.04
sudo /etc/init.d/ssh restart
```

로컬로 이동하기 위해서 서버접속을 종료합니다.

```bash
exit
```

root 로 로그인 시도를 해봅니다.

```shell
ssh root@example.com
root@example.com: Permission denied (publickey).
```
**'root@example.com: Permission denied (publickey).'** 문구가 나오면서 접속을 할 수 없습니다.

storyg 계정에 접속하기 위한 키를 생성합니다.

```bash
ssh-keygen -b 4096 
Generating public/private rsa key pair.
Enter file in which to save the key (/Users/storyg/.ssh/id_rsa): 
Enter passphrase (empty for no passphrase): 
Enter same passphrase again: 
Your identification has been saved in id_rsa.
Your public key has been saved in id_rsa.pub.
The key fingerprint is:
SHA256:abc abc abc abc +4 storyg@mac.local
The key's randomart image is:
+---[RSA 4096]----+
|                 |
+----[SHA256]-----+
```

생성된 공개키를 확인하고 복사합니다.

```bash
cat ~/.ssh/id_rsa.pub
ssh-rsa AAAAB storyg@mac.local
```
서버에 접속합니다.

```bash
ssh storyg@example.com
```

생성된 키 쌍의 공개키를 등록합니다.

```shell
cd ~
mkdir .ssh
vim .ssh/authorized_keys
```

아까 복사했던 키를 넣어줍니다. 키는 한줄에 다 넣습니다.

```conf
ssh-rsa AAAAB storyg@mac.local
```

종료 후에 비밀번호를 입력하지 않아도 접속이 되는지 확인합니다. 기본적으로 ssh 키의 기본 위치를 사용하기 때문에 다음과 같이 사용합니다.

```shell
ssh storyg@example.com
```

명시적으로 사용하려면 다음과 같이 합니다.

```shell
ssh -i ~/.ssh/id_rsa storyg@example.com
```

키로 서버 비밀번호 없이 접속이 된다면 등록이 잘 된 것입니다.

PasswordAuthentication 를 no 설정하여 외부에서 비밀번호로 접속할 수 없도록 변경합니다.

```shell
sudo vim /etc/ssh/sshd_config

...
PasswordAuthentication no
...
:wq
```

로컬로 이동합니다.

```bash
exit
```

키없이 접속해봅니다.(id_rsa를 잠시 다른 곳으로 옴겨봅니다.)

```shell
mv ~/.ssh/id_rsa ~/.ssh/id_rsa_bu
```

접속 시도를 하면 실패할 것입니다.

```shell
ssh storyg@example.com
grpark@donutz.co: Permission denied (publickey).
```

다시 키를 기본 위치에 옮깁니다.

```shell
mv ~/.ssh/id_rsa_ub ~/.ssh/id_rsa
```

서버에 접속해봅니다.

```bash
ssh storyg@example.com
```

잘된다면 ssh key만 서버에 접속하도록 보안이 강화 된 것입니다.