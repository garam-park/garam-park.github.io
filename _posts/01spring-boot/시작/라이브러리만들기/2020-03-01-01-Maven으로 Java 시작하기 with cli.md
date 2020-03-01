---
layout: post_with_ad
title:  "[01]스프링부트 퀵스타트 - Maven으로 Java 시작하기 with CLI"
date:   2020-03-01 21:43:47 +0900
permalink : /스프링부트/시작/01-프로젝트-시작
categories: program code
tags : maven cli code project
---

회사에서 스프링 부트를 사용하고 있습니다. 그래서 스프링부트를 공부하면서 알게된 내용을 정리합니다. 시리즈로 스프링부트 + 메이븐을 통해서 협업할 수 있는 환경 설정 까지 간단하게 다루려고합니다.

## 이 포스트의 목표

* Maven 으로 프로젝트 생성
* 자바 실행

이 포스트에서는 메이븐 기반의 일반적인 자바 프로젝트를 생성하는 것에 대해서 설명합니다. 자바 프로젝트를 생성한 이유는 자바 라이브러리 프로젝트로 사용하기 위해서 입니다.

## 이 포스트를 시작하기 전에

이 포스트는 다음의 부분에 대한 설명을 하지 않습니다.

* Java 설치
* maven 설치

### 프로젝트 생성

메이븐 기반의 자바 프로젝트를 설치하기 위해서 다음의 명령어를 실행합니다.

``` sh
mvn archetype:generate -DarchetypeArtifactId="maven-archetype-quickstart" -DarchetypeGroupId="org.apache.maven.archetypes" -DarchetypeVersion="1.4"
```

위의 명령어를 실행하면 다음과 같은 질문을 합니다.

``` sh
Define value for property 'groupId': co.storyg.blog
Define value for property 'artifactId': common
Define value for property 'version' 1.0-SNAPSHOT: : 
Define value for property 'package' co.storyg.blog: : co.storyg.blog.common
Confirm properties configuration:
groupId: co.storyg.blog
artifactId: common
version: 1.0-SNAPSHOT
package: co.storyg.blog.common
Y : [정확하게 입력했다면 엔터]
```

프로젝트 디렉토리로 이동합니다.

``` sh
cd common
```

메이븐 wrapper 설치를 하여 메이븐이 없는 환경에서도 사용할 수 있도록 설정합니다.

``` sh
mvn -N io.takari:maven:wrapper -Dmaven=[원하는 버전 입력]
```

> https://maven.apache.org/docs/history.html 에서 최신 버전을 확인 가능

메이븐 compile 을 하여 jar 파일을 빌드합니다.

``` sh
./mvnw compile
```

``` sh
[INFO] Scanning for projects...
[INFO] 
[INFO] ------------------------< co.storyg.foo:common >------------------------
[INFO] Building common 1.0-SNAPSHOT
[INFO] --------------------------------[ jar ]---------------------------------
[INFO] 
[INFO] --- maven-resources-plugin:3.0.2:resources (default-resources) @ common ---
[INFO] Using 'UTF-8' encoding to copy filtered resources.
[INFO] skip non existing resourceDirectory ./src/main/resources
[INFO] 
[INFO] --- maven-compiler-plugin:3.8.0:compile (default-compile) @ common ---
[INFO] Nothing to compile - all classes are up to date
[INFO] ------------------------------------------------------------------------
[INFO] BUILD SUCCESS
[INFO] ------------------------------------------------------------------------
[INFO] Total time:  0.304 s
[INFO] Finished at: 2020-02-29T08:30:06+09:00
[INFO] ------------------------------------------------------------------------
```
생성된 jar 파일을 실행합니다.

``` sh
java -cp $(pwd)/target/classes co.storyg.blog.common.App 
```

``` sh
Hello world
```