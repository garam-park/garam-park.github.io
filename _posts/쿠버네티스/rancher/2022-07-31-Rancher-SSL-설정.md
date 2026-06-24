---
layout: post_with_ad
title: "Rancher v2.5 SSL 설정"
date: 2022-07-31 18:57:01 +0900
permalink: "/쿠버네티스/rancher/ssl설정"
categories: kubernates 쿠버네티스, rancher, 랜처
tags: ssl tls https
lang: ko
description: "Rancher v2.5의 SSL(TLS) 설정 방법. 인증서 파일 위치와 적용 방법을 정리한 운영 메모입니다."
---

## Rancher v2.5 ssl(TLS) 설정

**ssl(TSL) 파일 위치**

path : `/etc/rancher/ssl`

**files**

`certbot`에서 다음과 같이 설정

* cacerts.pem : fullchain.pem 에 해당
* cert.pem : cert.pem 에 해당
* chain.pem : chain.pem 에 해당
* key.pem : privkey.pem 에 해당

