---
layout: post_with_ad
title: certbot 으로 tls 인증서 (ssl) 발급 하기
date: 2022-06-14 17:42:16 +0900
permalink: /운영/certbot/gen-tls
categories: 운영 devops
tags: certbot tls ssh
lang: ko
description: "certbot과 Docker로 Let's Encrypt TLS(SSL) 인증서를 발급하는 방법. 명령어와 볼륨 마운트 설정을 정리한 운영 메모입니다."
---

## certbot 으로 tls 인증서 발급 하기

``` sh
docker run --rm -it --name certbot \
    -v $(pwd)/example/etc:/etc/letsencrypt \
    -v $(pwd)/example/var:/var/lib/letsencrypt \
    certbot/certbot certonly \
    -d "example" \
    -d "*.example" \
    --manual \
    --preferred-challenges dns \
    --server https://acme-v02.api.letsencrypt.org/directory \
    -m admin@example
```
