---
layout: post_with_ad
title:  Maven으로 Java 시작하기 with cli
date:   2018-03-18 11:04:51 +0900
permalink : /Maven-으로-Java-시작하기
categories: program code
tags : maven cli code project
---

## 전제

* Java 설치
* maven 설치

### Project 빌드

메이븐 기반의 자바 프로젝트를 설치하기 위해서 다음의 명령어를 실행합니다.

``` sh
mvn archetype:generate -DarchetypeArtifactId="maven-archetype-quickstart" -DarchetypeGroupId="org.apache.maven.archetypes" -DarchetypeVersion="1.4"
```

위의 명령어를 실행하면 다음과 같은 질문을 합니다.

``` sh
Define value for property 'groupId': [그룹아이디 입력]
Define value for property 'artifactId': [아티팩트 아이디 입력]
Define value for property 'version' 1.0-SNAPSHOT: : [원하는 버전 입력]
Define value for property 'package' [입력된 그룹아이디]: : [패키지 입력]
Confirm properties configuration:
groupId: [입력된 그룹아이디]
artifactId: [입력된 아티팩트]
version: [입력된 버전]
package: [입력된 패키지]
Y : [정확하게 입력했다면 엔터]
```

프로젝트 디렉토리로 이동합니다.

``` sh
cd /path/to/project
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
java -cp $(pwd)/target/classes [입력된 패키지].App 
```

``` sh
Hello world
```