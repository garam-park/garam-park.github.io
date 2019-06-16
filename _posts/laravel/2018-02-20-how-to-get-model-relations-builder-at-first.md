---
layout: post_with_ad
title: "[Laravel] 라라벨 모델(Model) 관계(Relation)에서 빌더(builder) 처음에 생성하기"
date: 2018-02-20 18:44:51 +0900
permalink: /laravels/how-to-get-model-relations-builder-at-first
categories: 라라벨, laravel
tags : laravel, laravel builder, laravel model, laravel model builder, 라라벨, 라라벨 모델, 라라벨 모델 빌더, 라라벨 꿀팁,꿀팁
excerpt : 모델의 관계에서 빌더를 사용할 필요가 있다. 그럴 때 다음과 같은 예제를 사용해보자.
---

## **적용**

라라벨 모델을 다룰 때 정렬, 검색 등을 할 경우 모델로 부터 쿼리를 요청할 수 있습니다. 하지만 종종 넘어 오는 파라메터들의 성질 때문에 선택적으로 쿼리를 요청해야하는 경우가 있습니다. 그런 경우 다음과 같이 사용해 보세요.

[링크](/laravels/how-to-get-models-builder-at-first)

라라벨 모델의 관계에서도 빌더가 처음에 필요한 경우가 있습니다. 

```php?start_inline=true
$user = App\User::first();
$builder = $user->roles()->getQuery();
get_class($builder); #"Illuminate\Database\Eloquent\Builder"
```