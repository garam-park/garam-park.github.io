---
layout: post_with_ad
title:  certbot 로 tls(ssl|https) 와일드카드 인증서 발급하기
date:   2021-05-19 15:42:23 +0900
permalink : /path
categories: web infrastructure certbot
tags : ssl tls https letsencrypt certbot
---

아래의 명령어를 활용하면 certbot 으로 tls 인증서를 발급 가능

``` sh
docker run --rm -it --name certbot \
    -v $(pwd)/storyg.co/etc:/etc/letsencrypt \
    -v $(pwd)/storyg.co/var:/var/lib/letsencrypt \
    certbot/certbot certonly \
    -d "storyg.co" \
    -d "*.storyg.co" \
    --manual \
    --preferred-challenges dns \
    --server https://acme-v02.api.letsencrypt.org/directory \
    -m admin@storyg.co
```