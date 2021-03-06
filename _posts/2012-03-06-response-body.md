---
layout: post_with_ad
title: REST API Response Body 형식에 대한 경험적 구조
date: 2021-03-06 23:46:46 +0900
permalink: /rest-api-response-body-best-pratics
categories: rest
tags: restful, restful api, rest api, rest
---

필자는 다양한 REST API 설계 및 개발, 유지보수를 해왔고 그 경험을 바탕으로 간단하면서도 합리적은 Response 구조를 정립했습니다. 만약 더 개선 되어야 할 점이 발견된다면 이 포스트도 업데이트 될 것입니다.

# Response body 가 책임 져야 하는 것

response body 가 책임져야 하는 것은 API 를 사용하는 프로그램에 처리 결과를 간략하게 전달하는 것(code), 프로그램 코더, 개발자, 운영하는 자를 위한 메시지를 주는 것(message). 처리 결과 값(result)을 넘겨 주는 것이 될 수 있습니다.

필자는 이런 형식의 리턴 값을 추천합니다.

```javascript
{
	"code": 200000,
	"message": "ok",
	"result": {
		"foo":{}
		"somethings":[{},{}]
	}
}
```

1. `code` : 프로그램 코드 에서 사용. 처리 결과 상태.
2. `message` : 개발자가 문서를 보지 않아도 알 수 있는 message 값
3. `result` : API 가 전달해야하는 Resource 내용 혹은 처리 결과

## Code

HTTP 프로토콜을 보면 status code(상태 코드) 가 있는 것을 알 수 있습니다. 우리는 Browser 가 그 코드를 확인하고 어떻게 동작할 지 정하는 것 알고 있습니다. REST API 의 대상은 브라우저일 수 도 있지만 절대 다수는 전용 클라이언트 프로그램일 것입니다. HTTP 상태 코드는 브라우저를 위해서 설계되었습니다. REST API 는 HTTP 프로토콜에서 동작하긴 하지만 더 많은 것(비지니스 로직)을 표현하기 위해서 탄생했습니다. 그렇기 때문에 세자리로 되었고 이미 의미가 있는 상태 코드를 재활용하기는 어렵습니다. 필자는 5-6자리로 된 코드를 사용하길 권장합니다. 코드는 다음과 같이 구성하길 추천한다.

- **첫 세자리** : HTTP 프로토콜 상태 코드 - 200, 201, 404, 401, 412 등
- **넷째 짜리** : 타입 코드 - required, invalid, unsupported 등
- **마지막 두자리** : 구분 코드

마지막에 이해를 돕기위한 예시가 있습니다.

## Mesage

메시지는 코딩을 작성하는 코더 및 프로그래머와 같은 개발자들과 서비스를 운영하는 자를 위한 메시지입니다. 코드만 넘겨주면 즉각적인 해석을 하기 어렵고 개발문서를 확인해야 합니다. 하지만 개발 문서와 코드의 싱크는 잘 맞기 어렵습니다. API 는 개발자와 운영하는 자를 위해서 해당 메시지를 잘 전달 해야 합니다.

## Result

result 는 우리가 일반적으로 생각하는 body 에 들어가야 할 리소스나 혹은 시스템에 필요한 정보를 담아줍니다.

## 예시 - 사용자 등록

예시를 통해서 어떻게 사용하면 좋을 지 보도록 합시다. 다음은 사용자 등록(Register) API 호출 시 어떻게 디자인하면 좋을 지를 표현한 것입니다.

`POST` ~/register

```javascript
{
  "email": "foo@bar.baz",
  "password": "hellowrold!@"
}
```

위에 대한 응답은 다음과 같을 수 있다.

```javascript
// 정상적인 처리
{
  "code": 201000,
  // 201 는 HTTP Status code 에서 말하는 생성을 뜻
  // 000 은 아무의미 없이 자리를 맞춰주는 코드
  "message": "ok",
  "result": {
    "user": {
      // 반드시 resource 표현
      "id": 1,
      "email": "foo@bar.baz",
      "password": "hellowrold!@"
    }
  }
}
```

```javascript
// email 이 없을 경우
{
  "code": 412000,
  // 412 : 사전조건 실패
  // 0 : required param error
  // 00 : 이메일 - 임의로 00 은 이메일로 정한 것
  "message": "email Required in request body"
}
```

```javascript
// password 가 없을 경우
{
  "code": 412001,
  // 412 : 사전조건 실패
  // 0 : required param error
  // 01 : 패스워드 - 임의로 01 은 패스워드로 정한 것
  "message": "password Required in request body"
}
```

```javascript
// email 이 invalid 할 경우 - type 에러 등
{
  "code": 412100,
  // 412 : 사전조건 실패
  // 1 : invalid param error
  // 00 : 이메일 - 임의로 00 은 이메일로 정한 것
  "message": "email invalid"
}
```

```javascript
// password 가 invalid 할 경우 - type 에러 등
{
  "code": 412101,
  // 412 : 사전조건 실패
  // 1 : invalid param error
  // 01 : 패스워드 - 임의로 01 은 패스워드로 정한 것
  "message": "password invalid"
}
```

```javascript
// email format 에러
{
  "code": 412200, // 412(사전조건 실패)1(invalid)01(패스워드)
  // 412 : 사전조건 실패
  // 2 : param format error
  // 00 : 이메일 - 임의로 00 은 이메일로 정한 것
  "message": "unsupported email format"
}
```

```javascript
// password format 에러
{
  "code": 412201,
  // 412 : 사전조건 실패
  // 2 : param format error
  // 01 : 패스워드 - 임의로 01 은 패스워드로 정한 것
  "message": "unsupported password format"
}
```

```javascript
// 이미 등록된 이메일
{
  "code": 412300,
  // 412 : 사전조건 실패
  // 300 : 이미 등록된 이메일 에러 코드
  "message": "email already registered"
}
```

## 여러 가지 예상 질답

### 왜 code 가 숫자여야 하는가? 문자열이면 안되나?

물론 가능합니다. 예를들어 'EMAIL_REQUIRED' 라는 문자열을 하용하면 message 부분도 없앨 수 있다는 장점이 있습니다. 다음의 문제도 고려해 봅시다.

**코드는 고치기 어렵다**

code 값이 'EMAIL_REQUIRED' 와 같은 문자열로 디자인하고 작성했는데 오타가 나서 'EMAIL_REQ**IU**RED'로 프로그램이 작성되었다고 해봅시다. 그런데 아무도 눈치 못 채고 배포되었고 우리가 손 쓸 수 없는 3rd party 에서 사용하는 중간에 발견했습니다. 오타를 수정하면 에러와 장애가 일어날 게 뻔합니다. 또 다른 3rd party 에서는 문자열을 복사 붙여 넣기 하지 않고 의미 단위로 읽어 'EMAIL_REQ**IU**RED' 를 의미 단위로 올바르게 'EMAIL_REQUIRED'로 타입하고 배포를 했다고 해봅시다. 장애가 발생했지만 사람의 눈으로 찾기 매우 어렵게 됩니다. 'EMAIL_REQ**IU**RED' 를 뇌이징해서 'EMAIL_REQUIRED'으로 읽기 때문이다.

**swich 문**

code를 사용하는 가장 큰 부분은 에러가 발생했을 때에 처리입니다. 각 에러를 분기 해서 처리 해야 하고 적적한 것은 switch-case 를 활용하는 것입니다. swich-case 를 활용하려면 string 보다는 숫자가 좋습니다. 몇몇 언어에서는 string swich-case 를 제공하지 않습니다.

**HTTP 프로토콜 상에서만 동작하는 것이 아니다.**

HTTP 에서 상태코드가 존재하니 성공인지 실패인지 확실히 알 수 있어서 좋습니다. 하지만 HTTP 프로토콜이 아닌 다른 프로토콜에서도 성공인지 실패인지 단번에 알 수 있다는 보장이 없습니다. 그래서 어짜피 상태 코드와 같은 기능을 하는 것을 body 에 넣어 줘야 합니다. 이것이 result에 resoure 값을 넣는 이유도 됩니다.

### 왜 5~6자리 인가?

만약에 시스템이 작다면 5자리로 추천합니다. 타입 코드를 사용하지 않고 구분 코드만 사용하면 됩니다. 시스템을 세세한 구분을 하고 싶다면 6자리를 사용해서 타입 코드를 사용해도 무방합니다.

그렇지만 4자리로 처리하면 자리수가 너무 작습니다. 예상되는 에러가 10개가 넘을 가능성이 매우 높습니다. 하지만 100 개가 넘는다면 다시 API 설계에 문제가 있는 게 아닌가 고민해봐야 합니다.

### **Result 에 왜 resource 의 이름을 반드시 넣어야 한다고 하는 것인가?**

result 에 두개 이상의 resource 가 담길 수 있고(view model), pagination 과 같은 추가 정보도 포함 되어야 하기 때문입니다.

### Client 에서 Application 사용자에게는 무슨 메시지를 보여 줘야 하는가?

code 와 message 는 API 가 API 를 사용하는 프로그램과 개발자를 위한 것이고 Application 사용자를 위한 값은 주지 않습니다. 왜냐하면 그것은 CIient Application 의 몫(책임)이기 때문입니다. CIient Application 개발자가 적절하게 처리해 주어야 합니다.
