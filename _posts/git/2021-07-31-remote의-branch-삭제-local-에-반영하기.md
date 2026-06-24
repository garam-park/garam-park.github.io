---
layout: post_with_ad
title: "[git] remote의 branch 삭제 local 에 반영하기"
date: 2021-07-31 19:07:23 +0900
permalink: /git/remote의-branch-삭제-local-에-반영하기
categories: git
tags: git remote branch
lang: ko
description: "원격에서 삭제된 Git 브랜치를 로컬에 반영하는 방법. git remote prune origin과 git remote update --prune 명령어 사용법을 간단히 정리합니다."
---

remote 브랜치가 삭제 되었을 때, 로컬에 삭제된 상태가 반영을 시킬 필요가 있는 경우 다음의 명령어를 사용한다.

```sh
 git remote prune origin
```

```sh
 git remote update --prune
```
