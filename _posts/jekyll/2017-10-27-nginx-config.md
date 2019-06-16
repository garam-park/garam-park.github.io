---
layout: post_with_ad
title:  "[jekyll] Nginx 설정하기"
date:   2017-10-27 07:40:38 +0900
permalink : /jekylls/nginx-config
categories: jekylls
tags : jekyll,Nginx, jekyll nginx-config
excerpt : Nginx에서 Vue-router를 호스팅하기 위해서 다음의 코드 조각을 사용합니다.
---

## **jekyll 용 Nginx 설정**

Nginx에서 jekyll를 호스팅하기 위해서 다음의 코드 조각을 사용합니다.

```nginx
server {
    listen 80;

    root /path-to/keylls/_site;
    index index.html index.htm;
    server_name exmaple.com;
    access_log /var/log/nginx/exmaple.com.log;

    if (!-f "${request_filename}index.html") {
        rewrite ^/(.*)/$ /$1 permanent;
    }

    if ($request_uri ~* "/index.html") {
        rewrite (?i)^(.*)index\.html$ $1 permanent;
    }   

    if ($request_uri ~* ".html") {
        rewrite (?i)^(.*)/(.*)\.html $1/$2 permanent;
    }

    location / {
        try_files $uri.html $uri $uri/ /index.html;
    }
}
```