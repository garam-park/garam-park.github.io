---
layout: post_with_ad
title: javascript 용 tdlib 빌드 dockerfile
date: 2022-07-31 19:10:26 +0900
permalink: /etcs/
categories: telegram 
tags: tblib dockerfile
---

``` dockerfile
FROM ubuntu:22.04 AS builder

RUN apt-get update
RUN apt-get upgrade -y

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get -yq install make git zlib1g-dev libssl-dev gperf php-cli cmake g++

RUN git clone https://github.com/tdlib/td.git
RUN rm -rf /td/build
RUN mkdir /td/build

WORKDIR /td/build
RUN cmake -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX:PATH=../tdlib ..

RUN cmake --build . --target prepare_cross_compiling
RUN cd /td && php SplitSource.php
RUN cmake --build . --target install
RUN cd /td && php SplitSource.php --undo
RUN mkdir /app
RUN cp libtdjson.* /app

RUN apt-get install curl
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash -
RUN apt-get install nodejs -y

```
