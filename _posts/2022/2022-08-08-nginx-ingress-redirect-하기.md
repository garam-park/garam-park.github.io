---
layout: post_with_ad
title: nginx ingress path 값 그대로 redirect 하기
date: 2022-08-08 09:26:57 +0900
permalink: /etc/nginx-ingress-redirect-하기
categories: k8s kubernates
tags: ingress
lang: ko
description: "Kubernetes nginx ingress에서 경로(path)를 유지한 채 다른 도메인으로 리다이렉트하는 방법. rewrite-target 어노테이션과 request_uri 활용법을 정리합니다."
---

아래 처럼하면 도메인 변경되어 동일하게 동작게 리다리렉트 가능

`nginx.ingress.kubernetes.io/rewrite-target` : `https://example.com$request_uri`
