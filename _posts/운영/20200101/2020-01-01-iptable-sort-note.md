---
layout: post_with_ad
title:  iptables 방화벽 포트 관리(열기/닫기)
date:   2020-01-01 11:04:51 +0900
permalink : /운영/iptables/iptables-방화벽-관리
categories: web os linux
tags : operation, iptables, linux, iwinv
excerpt : iwinv 에서 방화벽 처리 삽질 해결
---

<!-- ## **방화벽** -->

<!-- iwinv 에서 인스턴스를 생성하면 관리 콘솔에서 방화변 설정을하지 않았어도 기본적으로 `iptables` 로 방화벽이 되어있습니다. 그래서 `iptables` 에서 해당 포트를 열어줘야 합니다. 그것 때문에 어이없는 시간 끌기가 되어 버린 경우가 많았죠..

전 16.04 우분투 인스턴스를 활용하고 검색을 통해서 얻은 정보를 정리해보았습니다. -->

**NOTE!!** 

    22번 포트 등 접속에 관련된 포트를 막는 일은 없어야 겠습니다.
    명령은 `root` 권한으로 실행합니다.

### iptable 상태 확인

아래의 명령어로 모든 체인의 규칙이나 특정 체인의 규칙을 알 수 있습니다.

``` sh
iptables --list
iptables -L
```

* --list or -L 옵셕

### 포트 열기

```
# 10080 포트를 들어오는 ACCEPT 규칙을 추가
iptables -I INPUT -p tcp --dport 10080 -j ACCEPT 
# 10080 포트를 나가는 ACCEPT 규칙을 추가
iptables -I OUTPUT -p tcp --dport 10080 -j ACCEPT 
```

* -I(--insert) : 새 규칙 추가
* -p(--protocol) : 프로토콜
* --dport : 목적 포트
* -j : 규칙 대상 (ACCEPT, DROP, QUEUE, RETURN 등 가능)

#### 포트 닫기

```
# 10080 포트를 막는 DROP 규칙을 추가
iptables -D INPUT -p tcp --dport 10080 -j DROP 
# 10080 포트를 막는 DROP 규칙을 추가
iptables -D OUTPUT -p tcp --dport 10080 -j DROP 
```

* -D(--delete) : 규칙 없애기