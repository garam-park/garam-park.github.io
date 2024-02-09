---
layout: post_with_ad
title: nginx ingress path 값 그대로 redirect 하기
date: 2022-08-08 09:26:57 +0900
permalink: /etc/nginx-ingress-redirect-하기
categories: k8s kubernates
tags: ingress
---

아래 처럼하면 도메인 변경되어 동일하게 동작게 리다리렉트 가능

`nginx.ingress.kubernetes.io/rewrite-target` : `https://example.com$request_uri`
