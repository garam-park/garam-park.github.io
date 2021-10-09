---
layout: post_with_ad
title: "php7.4 docker 에서 GD extension 설치하기"
date: 2021-10-09 11:46:58 +0900
permalink: /phps/install-php74-gd-in-docker
categories: php docker
tags: php docker install gd extension
excerpt: --with-jpeg --with-freetype
---

## 배경

현재 진행 중인 프로젝트에서 이미지 관련 리사이즈를 하기 위해서 검색하면서 [smottt/wideimage](https://packagist.org/packages/smottt/wideimage) 현재 상황에서 적절한 라이브러리라 판단하고 적용했지만 gd 확장을 사용이 필요했다. 얼마전에 맥북프로로 개발환경을 고치면서 익숙하지 않은 php 환경을 하느라 고생했는데 맥에서 brew 로 php 설치하면 gd 가 자동으로 설치가 되는 것 같다. pre-production 에서 배포를 하지 않았다면 큰 문제가 발생했을 수도 있었다. 하지만 pre-production을 도입하기를 잘 한듯 하다.

## 문제 해결

pre-production 환경에서 extention 이 없어서 발생한 에러이기 때문에 간단하게 dockerfile 에 extention 를 설치하면 가볍게 해결될 것이라고 생각했다.

### 검색

`php gd install docker` 키워드로 구글 검색으로 [스텍오버플로우](https://stackoverflow.com/questions/39657058/installing-gd-in-docker)의 포스트를 참고해서 dockerfile를 수정했다.

현재 docker 기반 이미지를 php:7-fpm 을 사용하고 있었고, 관련한 답변도 있었다. 그 답변에 있는 내용은 다음과 같았다.

``` docker
FROM php:7-fpm

RUN docker-php-ext-install mysqli pdo pdo_mysql
RUN apt-get update -y && apt-get install -y libwebp-dev libjpeg62-turbo-dev libpng-dev libxpm-dev \
    libfreetype6-dev
RUN apt-get update && \
    apt-get install -y \
        zlib1g-dev 

RUN docker-php-ext-install mbstring

RUN apt-get install -y libzip-dev
RUN docker-php-ext-install zip

RUN docker-php-ext-configure gd --with-gd --with-webp-dir --with-jpeg-dir \
    --with-png-dir --with-zlib-dir --with-xpm-dir --with-freetype-dir \
    --enable-gd-native-ttf

RUN docker-php-ext-install gd

CMD ["php-fpm"]

EXPOSE 9000
```

여기서 필요한 부분을 다음과 같이 판단하고

```jsx
RUN docker-php-ext-configure gd --with-gd --with-webp-dir --with-jpeg-dir \
    --with-png-dir --with-zlib-dir --with-xpm-dir --with-freetype-dir \
    --enable-gd-native-ttf

RUN docker-php-ext-install gd
```

현재 dockerfile 에 추가했다. 하지만 동작하지 않았다. 수 시간의 삽질 끝에 [php.net](http://php.net) 에서 관련 정보를 얻을 수 있었다. ([링크](https://www.php.net/manual/en/image.installation.php))

```jsx
To enable support for jpeg add --with-jpeg-dir=DIR. Jpeg 6b, 7 or 8 are supported. As of PHP 7.4.0, use --with-jpeg instead.
```

```jsx
To enable support for png add --with-png-dir=DIR. Note, libpng requires the zlib library, therefore add --with-zlib-dir[=DIR] to your configure line. As of PHP 7.4.0, --with-png-dir and --with-zlib-dir have been removed. libpng and zlib are required.
```

이외 다양한 참고 사항들....

### 결론

결론적으로는 다음의 설정으로 해결했다.

```docker
# GD
# Setup GD extension
RUN apt-get install -y libfreetype6-dev libjpeg62-turbo-dev libpng-dev
RUN docker-php-ext-configure gd --with-freetype --with-jpeg
RUN docker-php-ext-install gd
RUN docker-php-ext-enable gd
```
