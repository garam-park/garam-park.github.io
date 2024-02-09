---
layout: post_with_ad
title: "[git] 현재 해더의 tag 값 가져오기"
date: 2022-06-15 06:57:23 +0900
permalink: /git/remote의-branch-삭제-local-에-반영하기
categories: git
tags: git tag describe
---

### 기본

```sh
git tag -l | grep $(git describe HEAD)
```

### 응용 - Shell Script

``` sh
export VERSION="$(git tag -l | grep $(git describe HEAD))"

if [ -z "$VERSION" ]; then
    echo "\$VERSION is empty"
    exit 1
fi
```

ref : 스택오버플로우(https://stackoverflow.com/questions/2324195/how-to-get-tags-on-current-commit)