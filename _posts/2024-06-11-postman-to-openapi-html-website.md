---
layout: post_with_ad
title: 개발 과정에서 Postman을 OpenAPI로 배포하기
date: 2024-06-11 11:23:00 +0900
permalink: /publish-openapi-from-postman
categories: web api
tags: restful, restful api, rest api, rest
---

## 개발 과정에서 Postman을 OpenAPI로 배포하기

오늘은 개발 과정에서 Postman을 OpenAPI로 전환하는 방법에 대해 이야기해보겠습니다.

### 배경 설명

최근 우리 팀은 Postman을 활용하여 API 개발을 진행하고 있었습니다. Postman은 강력한 기능과 편리한 인터페이스를 제공하지만, **유료 결제를 해야 하는 단점**이 있었습니다. 팀원들의 이해도가 낮고 비용도 높아서 Postman을 계속 사용하기에는 어려움이 있었죠.

또한, Postman Collection과 Environment를 export/import하는 것도 쉽지 않았습니다. 팀원들 간에 공유하고 동기화하는 데 어려움이 있었습니다.

![](/images/2024/06/11-1.png){:style="width:100%"}

매번 export 하고 버전 관리하는게 여간 힘든 일(유료 결제는 생각보다 비싸서 하기 싫다)

### OpenAPI로 전환하기

그러던 중 우리는 OpenAPI 문서를 바로 배포해주는 **'Redocly'라는 서비스를 발견**했습니다. 만약 Postman을 OpenAPI로 전환할 수 있다면, 유료 결제 없이도 API 문서를 쉽게 공유하고 관리할 수 있을 것 같았습니다.

다행히도 Postman에서 제공하는 'postman-to-openapi' 도구를 통해 Postman Collection을 OpenAPI 형식의 YAML 파일로 변환할 수 있었습니다. 이 YAML 파일을 Redocly에 업로드하면 자동으로 HTML 문서로 렌더링되어 웹에서 바로 확인할 수 있었습니다.

### 과정 요약

1. Postman에서 API 개발 및 테스트
2. `postman-to-openapi` 도구를 사용하여 Postman Collection을 OpenAPI YAML 파일로 변환
3. Redocly에 YAML 파일을 업로드하여 HTML 문서로 렌더링
4. 웹에서 API 문서 확인 및 공유

### 결과

이렇게 해서 우리는 Postman을 OpenAPI로 성공적으로 전환할 수 있었습니다. 이제 유료 결제 없이도 API 문서를 쉽게 공유하고 관리할 수 있게 되었죠. 팀원들 간의 협업도 더욱 원활해졌습니다.

여러분도 개발 과정에서 Postman을 사용하고 계신다면, OpenAPI로 전환해보는 것을 고려해보세요. 비용 절감과 더불어 API 문서 관리의 편의성도 높일 수 있을 것입니다.