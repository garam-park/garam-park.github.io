---
layout: post_with_ad
title:  REST API를 알아보자
date:   2018-03-18 11:04:51 +0900
permalink : /rest-api-explain
categories: web api
tags : restful, restful api, rest api, rest
excerpt : RESTful Api를 알아봅시다.
---

## **목차**

1. 소개
1. 구성요소
1. 규칙 

## **1 소개**

### REST란 ? 

**Re**presentational **S**tate **T**ransfer 를 짧게 쓰는 단어인데요. 표현방법 전달 하기 정도로 해석할 수 있습니다. REST에서 하나 생략된 단어가 있습니다. Resource 입니다. 표현 상태 전이란 뜻은 어딴 대상의 상태를 표현해서 넘겨준다는 뜻입니다.
### **1.1 Representational : 표현**

`표현`이라는 뜻은 대상(Resource)를 다양한 방법으로  나타내겠다는 의미입니다. 표현 방법으로 `json`,`xml`,`csv` 등이 있습니다.

### **1.2 State : 상태**

대상(resource)의 상태는 실질적인 정보입니다. 대상의 상태를 표현한다면 그 자체가 정보가 됩니다.

### **1.3 Transfer : 전이|전달**

전달이라는 뜻은 네트워크를 통해서 전달한다는 뜻입니다.

## **2 웹의 구조적 스타일(Web’s archietectural Style)**

REST API는 HTTP 프로토콜 상에서 동작하는 API이기 때문에 HTTP 프로토콜의 제약사항 혹은 이점들을 사용할 수 있습니다.

1. 클라이언트/서버( Client / Server )
1. 정형화된 인터페이스 ( Uniformed Interface ) 
1. 계층 시스템 ( Layered System )
1. 캐시 ( Cache )
1. 상태 없음 ( Stateless )
1. 주문형 코드 ( code-on-command)

### **2.1 클라이언트/서버( Client / Server )**

웹은 클라이언트와 서버로 이뤄져있습니다. 그리고 서버와 클라이언트는 독립적입니다. 독립적이라는 뜻은 서로가 서로에게 영향을 미치지 않는다는 겁니다. 서로가 통신하는 것은 철저하게 프로토콜(약속)에 의한 것이고 그 약속만 지킨다면 서버가 어떤 언어로 구현되었는지 클라이언트가 어떤 언어로 구현 되었는지 중요하지 않습니다.

### **2.2 정형화된 인터페이스 ( Uniformed Interface )**

+ 리소스 식별 - URI(Unified Resource Indentity)
+ 표현을 통한 리소스 처리  - HTML/JSON/XML
+ 자기서술적 메시지 - 요청은 메시지 / 헤더의 메타테이터

웹에서는 URI를 통해서 리소스를 구별(구분)하고 해더의 `Content-type` 등을 통해서 표현하는 방식과 표현 대상의 메타정보를 포함할 수 있습니다.

### **2.3 계층 시스템 ( Layered System )**

웹에서는 다양한 계층으로 이뤄져 있기 때문에 보안 및 부하 처리를 할 수 있습니다.

### **2.4 캐시 ( Cache )**

웹에서는 콘텐츠 전송망 CDN 단, 또는 클라이언트 내에도 가능 캐시를 제공합니다.
### **2.5 상태 없음 ( Stateless )**

웹에서는 서버가 클라이언트의 상태를 관리할 필요가 없습니다. 필요하다면 해당 상황에 대한 정보를 클라이언트에서 직접 관리합니다.

### **2.6 주문형 코드 ( code-on-command )**
내용 없음

## **3 규칙**

### **3.1 URI 식별자 설계**

+ URI 기본 원칙
+ URI vs URL
+ 리소스 형식 (Resource Type) 
  + 도큐먼트 ( Document )
  + 컬렉션 ( Collection )
  + 스토어 ( Store )
  + 컨트롤러 ( Controller )
+ 명명 규칙 (Conventional Naming Rules)
+ Query  : 선택 사항

+ HTTP 프로토콜 이용
  + HTTP 프로토콜의 이용
  + 요청 메서드
  + 응답 상태 코드
