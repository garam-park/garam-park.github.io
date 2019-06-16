---
layout: post_with_ad
title:  "[VueJs] Vue-Router Nginx 설정하기"
date:   2017-10-27 07:25:57 +0900
permalink : /vue-js-posts/vue-router-nginx-config
categories: vuejs
tags : vue, vuejs, tutorial, restful, vuejs, 튜토리얼, 예제 연습, vuejs 입문, Vue js 입문, VueJs 튜토리얼, Nginx
excerpt : Nginx에서 Vue-router를 호스팅하기 위해서 다음의 코드 조각을 사용합니다.
---

## **vue-router 용 Nginx 설정**

Nginx에서 Vue-router를 호스팅하기 위해서 다음의 코드 조각을 사용합니다.

```nginx
server {

  listen 80;
  listen [::]:80;

  root /path/to/vue;

  index index.html;

  server_name vue-router.example.com;

  location / {
    try_files $uri $uri/ @rewrites;
  }

  location @rewrites {
    rewrite ^(.+)$ /index.html last;
  }

  location ~* \.(?:ico|css|js|gif|jpe?g|png)$ {
    expires max;
    add_header Pragma public;
    add_header Cache-Control "public, must-revalidate, proxy-revalidate";
  }

}
```