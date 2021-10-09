---
layout: post_with_ad
title: "Install gd extension on php7.4 in Docker"
date: 2021-10-09 11:46:58 +0900
permalink: /phps/eng/install-php74-gd-in-docker
categories: php docker
tags: php docker install gd extension
excerpt: use `--with-jpeg`, not `--with-jpeg-dir`, use `--with-freetype`, not `--with-freetype-dir`
---

**Note**

- use `--with-jpeg`, not `--with-jpeg-dir`
- use `--with-freetype`, not `--with-freetype-dir`

### Example

```docker
# GD
# Setup GD extension
RUN apt-get install -y libfreetype6-dev libjpeg62-turbo-dev libpng-dev
RUN docker-php-ext-configure gd --with-freetype --with-jpeg
RUN docker-php-ext-install gd
RUN docker-php-ext-enable gd
```

refs : [stackoverflow](https://stackoverflow.com/questions/39657058/installing-gd-in-docker), [php.net](https://www.php.net/manual/en/image.installation.php)