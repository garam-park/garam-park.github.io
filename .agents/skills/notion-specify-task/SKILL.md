---
name: notion-specify-task
description: >-
  Turn the existing analysis for exactly one StoryG Blog task already in 명세 and identified by an explicit exact task ID into an implementation-ready review draft, save only the managed section of that Notion task body, and set 명세리뷰 to 리뷰전 without waiting for human approval. Use when the user supplies `작업 ID: ID값` and asks to draft, prepare, revise, or automatically continue the task specification workflow. Stop before specification review or implementation.
---

# Notion 할 일 명세 초안 작성

분석 결과를 구현 가능한 명세 초안으로 정리해 대상 Notion 할 일의 관리 구역에 저장하고 `명세리뷰=리뷰전`으로 둔 뒤 멈춘다.

## 작업 ID 계약

- 현재 요청에 `작업 ID: <정확한 값>`과 같은 ID의 분석 결과가 반드시 있어야 한다.
- 이전 대화, 제목, URL, 페이지 UUID만으로 대상을 추론하지 않는다.
- 데이터베이스 `ID` unique_id에 exact match하고 StoryG Blog relation을 확인한다.
- ID가 누락되거나 분석·페이지 ID가 다르면 쓰지 않는다.

## 권한과 경계

정확한 작업 ID를 포함해 이 스킬을 실행해 달라는 요청은 다음을 승인한 것으로 본다.

- 대상 본문의 ``notion-specify-project-task/v1`` 관리 구역 생성 또는 초안 갱신
- `명세리뷰`를 `리뷰전`으로 설정

다음은 하지 않는다.

- 사용자 작성 본문, 다른 관리 구역, 다른 Notion 속성·페이지 변경
- 명세 자동 확정 또는 `리뷰완료` 변경
- 코드·파일·branch·worktree·commit·push·PR·CI·배포 변경
- 명세 저장 뒤 구현 시작

Notion에는 이 저장소 `.codex/config.toml`의 이름이 정확히 `notion`인 MCP만 사용한다. 노출된 도구 이름이 있다면 `mcp__notion__...`만 허용한다. 다른 Notion 플러그인, `mcp__codex_apps__notion`, 브라우저 자동화, 직접 API 호출로 우회하지 않는다.

## 고정 대상

| 대상 | 값 |
| --- | --- |
| 프로젝트 | `StoryG Blog` |
| 프로젝트 페이지 ID | `3a48e829-7400-81a5-9f3c-cfd701dd3c6c` |
| 할 일 data source ID | `3a28e829-7400-80b2-80bf-000bb0ab59ac` |
| 연결 속성 | `프로젝트` |
| 명세 리뷰 속성 | `명세리뷰` |
| 초안 값 | `리뷰전` |

실행할 때 data source와 옵션을 다시 읽고 이름·유형·값이 일치하는지 확인한다.

## 실행 순서

### 1. 입력 검증

입력한 작업 ID를 exact match한다. 분석의 사실, 추론, 열린 질문을 구분하고 분석 ID와 실제 TODO ID가 같은지 확인한다.

다음 경우에는 쓰지 않는다.

- 대상 TODO를 하나로 식별할 수 없음
- StoryG Blog 작업이 아님
- 최신 상태가 정확히 `명세`가 아님
- 분석이 없거나 다른 작업의 결과임
- 목표 자체를 정해야 하는 중대한 제품 질문이 남아 있음

`백로그`, `시작 전`, `일시중단`을 이 단계에서 `명세`로 바꾸지 않는다. 먼저 `$notion-analyze-task`를 실행한다. `진행 중` 이후 상태도 되돌리지 않는다.

### 2. 명세 초안 작성

아래 관리 구역 전체를 작성한다.

```markdown
## Codex 구현 명세

`notion-specify-project-task/v1`

명세 상태: 검토 초안
확정 방식: 자동 검토 대기

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

- 완료 조건을 검증 가능한 체크리스트로 작성한다.
- 확인되지 않은 내용은 가정이나 열린 질문으로 표시한다.
- 파일 경로는 저장소에서 확인한 경우에만 적는다.
- 구현 방법보다 결과와 제약을 중심으로 작성한다.
- 사람의 제품 결정이 필요한 열린 질문은 숨기지 않는다.

### 3. 초안 저장

쓰기 직전에 페이지와 스키마를 다시 읽는다.

- 관리 구역이 없으면 본문 끝에 한 번 추가한다.
- 관리 구역이 하나이고 아직 `검토 초안`이면 내용이 달라질 때만 해당 구역을 교체한다.
- 동일한 검토 초안이면 본문을 다시 쓰지 않고 누락된 `명세리뷰=리뷰전`만 복구한다.
- 관리 구역이 이미 `확정`이면 본문과 `명세리뷰`를 자동으로 되돌리지 않고 `$notion-review-spec` 또는 `$notion-implement-task`로 인계한다.
- marker가 둘 이상이면 쓰지 않는다.
- 사용자 작성 영역과 다른 관리 구역을 덮어쓰지 않는다.

본문을 쓰기 직전에 상태가 여전히 `명세`인지 다시 확인한다. 검토 초안인데 `명세리뷰=리뷰완료`이면 본문이나 속성을 자동으로 내리지 않고 불일치를 보고한다.

그 외에는 관리 구역을 저장한 뒤 재조회해 초안과 기존 본문 보존을 확인한다. 검토 초안의 `명세리뷰`가 이미 `리뷰전`이면 중복 쓰지 않고, 비어 있으면 `리뷰전`으로 변경한다.

### 4. 결과 검증

다음을 재조회한다.

1. marker가 정확히 하나임
2. `명세 상태: 검토 초안`임
3. 저장된 구역이 생성한 초안과 일치함
4. `명세리뷰`가 `리뷰전`임
5. `상태`가 `명세`로 유지됨
6. 사용자 본문과 다른 속성이 보존됨

실패하면 추가 쓰기를 반복하지 않고 실제 상태와 재개 지점을 보고한다.

## 완료 조건

같은 작업 ID의 명세 초안이 정확히 한 번 저장되고 `상태=명세`, `명세리뷰=리뷰전`으로 검증되면 끝낸다.

```text
다음 호출: $notion-review-spec 작업 ID: <정확한 값>
```
