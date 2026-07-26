---
name: notion-analyze-task
description: >-
  Start specification work for exactly one eligible StoryG Blog Notion task identified by an explicit exact task ID by moving it idempotently to 명세, then analyze its purpose, scope, requirements, acceptance criteria, repository impact, risks, validation plan, and open questions without changing files or later-stage artifacts. Use after notion-select-task returns an ID, to resume a task already in 명세, or when the user explicitly asks to analyze one pre-implementation task.
---

# Notion 할 일 명세 분석

사용자가 명시한 정확한 작업 ID 하나를 명세 단계로 전환하고 저장소 영향을 분석해 명세화에 필요한 재료를 제공한 뒤 멈춘다.

## 작업 ID 계약

- 현재 요청에 `작업 ID: <정확한 값>`이 반드시 있어야 한다.
- 이전 대화에서 선택한 작업, 제목, 순서, URL, 페이지 UUID를 작업 ID 대신 추론하지 않는다.
- 데이터베이스 스키마에서 작업 식별자 속성을 확인하고 입력값을 exact match한다.
- 결과가 정확히 한 개이고 StoryG Blog relation을 가질 때만 진행한다.
- 누락, 0건, 중복, relation 불일치면 분석하지 않고 정확한 작업 ID를 요청한다.

## 권한과 경계

정확한 작업 ID를 포함한 호출은 대상 작업의 `상태`를 `명세`로 변경하는 것만 승인한 것으로 본다.

- Notion 페이지, 데이터베이스, 다른 속성·본문과 저장소는 읽기 전용으로 확인한다.
- 다른 작업을 탐색하거나 대신 선택하지 않는다.
- 대상 작업의 다른 속성·본문·댓글을 변경하지 않는다.
- 파일 수정, branch·worktree 생성, commit, push, PR, CI, 배포를 하지 않는다.
- 명세를 확정하거나 구현을 시작하지 않는다.

Notion에는 이 저장소 `.codex/config.toml`의 서버 이름이 정확히 `notion`인 MCP 조회 도구만 사용한다. 노출된 도구 이름이 있다면 `mcp__notion__...`만 허용한다. 다른 Notion 플러그인, `mcp__codex_apps__notion`, 브라우저 자동화, 직접 API 호출로 우회하지 않는다.

## 고정 대상

| 대상 | 값 |
| --- | --- |
| 프로젝트 | `StoryG Blog` |
| 프로젝트 페이지 ID | `3a48e829-7400-81a5-9f3c-cfd701dd3c6c` |
| 할 일 데이터베이스 ID | `3a28e829-7400-808f-b53b-c35b8fef93a8` |
| 현재 data source ID | `3a28e829-7400-80b2-80bf-000bb0ab59ac` |
| 연결 속성 | `프로젝트` |
| 상태 속성 | `상태` (`status`) |
| 명세 상태 | `명세` |
| 저장소 | `/Users/garam/ws/garam/garam-park.github.io` |

## 실행 순서

### 1. 대상·스키마·단계 검증

입력한 작업 ID를 exact match해 대상 페이지를 확정한다. 모든 속성과 본문, 필요한 상위·하위·선행·후행 관계를 읽는다. data source의 `상태`가 status 유형이고 `명세` 옵션이 실제로 존재하는지 확인한다.

허용되는 시작 상태는 `백로그`, `시작 전`, `일시중단`, `명세`뿐이다.

- `명세`이면 상태를 다시 쓰지 않고 재개한다.
- `진행 중`, `주제 검토 요청`, `검토 중`, `완료`, `취소`, `보관`, `모니터링`은 `명세`로 되돌리지 않는다.
- PR 연결 marker, 검증된 작업 branch·worktree, open PR처럼 구현 이후의 일관된 산출물이 있으면 현재 상태가 앞 단계여도 `명세`로 내리지 않고 `$notion-run-queue`의 산출물 기반 재개 판정을 요청한다.
- `명세` 옵션이 없거나 대상·relation·상태를 확정할 수 없으면 변경과 분석을 시작하지 않는다.

### 2. 명세 상태 전환

쓰기 직전에 대상 페이지를 다시 읽는다.

- 최신 상태가 `백로그`, `시작 전`, `일시중단`이고 이후 단계 산출물이 없을 때만 `상태.status.name`을 `명세`로 변경한다.
- 최신 상태가 이미 `명세`면 no-op으로 처리한다.
- 다른 상태로 바뀌었으면 덮어쓰지 않는다.

갱신 뒤 페이지를 재조회해 상태가 정확히 `명세`인지 확인한다. 확인되지 않으면 저장소 분석을 시작하지 않는다. 상태 변경 뒤 이후 분석이 실패하더라도 상태를 되돌리지 않고 같은 작업 ID의 분석 단계부터 재개한다.

Notion의 read-then-write는 동시 실행 잠금이 아니다. 동일 프로젝트에서 다른 자동 큐가 실행 중이면 상태를 쓰지 않는다.

### 3. 저장소 조사

`AGENTS.md`, 관련 코드·문서·테스트, 최근 이력, 현재 작업 트리 상태를 읽기 전용으로 확인한다. 제목의 단어만으로 범위를 단정하지 말고 `rg`로 실제 관련 경로와 기존 동작을 찾는다.

### 4. 명세 분석

다음 항목을 사실, 추론, 열린 질문으로 구분해 정리한다.

1. 작업 ID, 제목, 상태 `명세`, Notion 링크
2. 문제와 배경
3. 기대 결과와 사용자 가치
4. 범위와 비범위 후보
5. 기능·콘텐츠·운영 요구사항 후보
6. 검증 가능한 완료 조건 후보
7. 예상 변경 파일과 기존 동작
8. 테스트·검증 계획 후보
9. 의존성, 위험, 호환성
10. 명세화 전에 결정할 열린 질문

불명확한 내용을 사실처럼 채우지 않는다. 구현 방식을 필요 이상으로 고정하지 않고, 다음 단계에서 명세로 확정할 결정과 근거를 분리한다.

### 5. 인계

마지막에 동일한 ID를 포함한 다음 호출을 제공한다.

```text
다음 호출: $notion-specify-task 작업 ID: <정확한 값>
```

## 완료 조건

다음을 모두 만족하면 끝낸다.

- 대상 작업의 상태가 재조회 결과 `명세`
- 명시된 한 작업의 명세 분석 보고서와 다음 호출이 제공됨
- 대상 `상태` 외 Notion 내용과 저장소가 실행 전과 동일함
