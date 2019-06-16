---
layout: post_with_ad
title:  "공분산"
permalink : /python/covariance
date:   2018-02-11 21:49:02 +09:00
categories: python3 covariance
tags :  python
excerpt : 공분산의 개념을 알아보자
---

# **공분산**

## 공분산을 처음 부터 구하기

```python
# 평균
def mean(x): 
    return sum(x) / len(x)

# 평균과 각 요소의 차이
def de_mean(x):
    x_bar = mean(x)
    return [x_i - x_bar for x_i in x]

# 내적, 각 요소를 곱한다
def dot(v, w):
    return sum(v_i * w_i for v_i, w_i in zip(v, w))

# 공분산
def covariance(x, y):
    n = len(x)
    return dot(de_mean(x), de_mean(y)) / (n - 1)
```

## NumPy를 이용하여 공분산 구하기

```python
import numpy
numpy.cov(x,y)[0][1]
```