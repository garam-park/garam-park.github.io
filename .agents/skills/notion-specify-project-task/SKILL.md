---
name: notion-specify-project-task
description: Turn an existing StoryG Blog task analysis into a clear implementation specification and update only the managed section of the linked Notion task body after explicit user approval. Use when the user asks to organize analyzed findings in a Notion TODO, prepare an implementation-ready task description, revise an existing managed specification, or save an approved specification without starting implementation.
---

# Notion 프로젝트 할 일 명세화

분석 결과를 구현 가능한 명세로 정리하고, 사용자가 승인한 내용만 해당 Notion 할 일 본문에 반영한 뒤 멈춘다.

## 작업 경계

- 입력으로 기존 분석 결과와 대상 TODO ID 또는 Notion 페이지를 요구한다.
- 승인 전에는 Notion을 변경하지 않는다.
- 승인 후에는 대상 할 일 본문의 관리 구역만 생성하거나 갱신한다.
- Notion 상태, `명세리뷰`를 포함한 속성, 다른 페이지를 변경하지 않는다.
- 코드와 파일을 수정하거나 브랜치, commit, push, PR, CI, 배포 작업을 하지 않는다.
- 명세 저장 뒤 구현을 시작하지 않는다.

Notion에는 이 저장소 `.codex/config.toml`의 서버 이름이 정확히 `notion`인 MCP만 사용한다. 노출된 도구 이름이 있다면 `mcp__notion__...`만 사용한다. 다른 Notion 플러그인, `mcp__codex_apps__notion`, 브라우저 자동화, 직접 API 호출로 우회하지 않는다. 프로젝트 Notion MCP를 사용할 수 없으면 중단하고 알린다.

## 고정 대상

| 대상 | 값 |
| --- | --- |
| 프로젝트 | `StoryG Blog` |
| 프로젝트 페이지 ID | `3a48e829-7400-81a5-9f3c-cfd701dd3c6c` |
| 할 일 데이터베이스 ID | `3a28e829-7400-808f-b53b-c35b8fef93a8` |
| 현재 data source ID | `3a28e829-7400-80b2-80bf-000bb0ab59ac` |
| 연결 속성 | `프로젝트` |

대상 할 일이 이 데이터베이스에 속하고 `프로젝트` relation으로 StoryG Blog에 연결됐는지 읽기 전용으로 검증한다. ID나 스키마를 추측하지 않는다.

## 실행 순서

### 1. 입력 검증

분석 결과에서 확인된 사실, 추론, 열린 질문을 구분한다. 대상 페이지의 속성과 현재 본문을 읽어 분석 대상과 실제 TODO가 같은지 확인한다.

다음 경우에는 본문을 갱신하지 않는다.

- 대상 TODO를 하나로 식별할 수 없음
- StoryG Blog에 연결된 할 일이 아님
- 분석 결과가 없거나 다른 TODO의 결과임
- 구현 방향을 바꾸는 중요한 질문이 남아 있음

### 2. 명세 초안 작성

아래 형식으로 관리 구역 전체를 작성한다.

```markdown
## Codex 구현 명세

`notion-specify-project-task/v1`

### 배경

### 목표

### 비범위

### 요구사항

### 완료 조건

### 예상 변경 대상

### 검증 계획

### 위험 및 의존성

### 열린 질문
```

- 완료 조건은 검증 가능한 체크리스트로 작성한다.
- 분석에서 확인되지 않은 내용은 사실처럼 쓰지 않고 가정 또는 열린 질문으로 표시한다.
- 파일 경로는 저장소에서 확인된 경우에만 구체적으로 적는다.
- 구현 방법을 과도하게 고정하지 말고 결과와 제약을 중심으로 쓴다.
- 중요한 열린 질문이 있으면 먼저 사용자와 해결하고 초안을 갱신한다.

### 3. 승인 대기

대상 TODO와 본문에 들어갈 관리 구역 전체를 사용자에게 보여 주고 다음을 명시적으로 확인한다.

> 이 명세로 Notion 할 일 본문을 갱신할까요?

“전체 진행”, 이전 단계 승인, 모호한 긍정은 본문 갱신 승인으로 간주하지 않는다. 승인은 정확한 TODO와 제시한 명세 내용에만 유효하다. 승인 뒤 내용이 실질적으로 바뀌면 다시 승인받는다.

### 4. 본문 갱신

쓰기 직전에 페이지 메타데이터와 본문을 다시 읽는다. 초안 작성 뒤 사용자가 본문을 변경했다면 최신 내용을 반영해 충돌 여부를 확인하고, 제안 명세가 달라지면 다시 승인받는다.

관리 구역은 제목 `## Codex 구현 명세`와 marker ``notion-specify-project-task/v1``로 식별한다.

- 관리 구역이 없으면 본문 끝에 한 번만 추가한다.
- 관리 구역이 하나면 그 구역만 정확히 교체한다.
- 같은 marker가 둘 이상이면 쓰지 말고 중복을 보고한다.
- marker 없는 기존 명세나 사용자 작성 영역을 덮어쓰거나 삭제하지 않는다.
- 페이지 전체 교체보다 기존 관리 구역의 정확한 find-and-replace 또는 끝 삽입을 우선한다.
- 승인된 명세와 무관한 서식 정리도 하지 않는다.

### 5. 결과 검증

갱신 뒤 페이지 본문을 다시 읽고 다음을 확인한다.

1. 관리 marker가 정확히 하나임
2. 저장된 관리 구역이 승인본과 일치함
3. 기존 사용자 본문이 보존됨
4. Notion 속성이 바뀌지 않음

검증에 실패하면 추가 쓰기를 반복하지 말고 실제 상태와 안전한 재개 지점을 알린다.

## 완료 조건

승인한 명세가 대상 Notion 할 일 본문에 정확히 한 번 저장되고 재조회로 확인되면 끝낸다. 구현, 상태 변경, 다음 단계 실행은 별도 스킬에 맡긴다.
