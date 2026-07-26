---
name: notion-analyze-task
description: Analyze the specification needs of exactly one StoryG Blog Notion task identified by an explicit exact task ID, without selecting a task or changing anything. Use after notion-select-task has returned an ID, or whenever the user supplies `작업 ID: ID값` and wants the task's purpose, scope, requirements, acceptance criteria, repository impact, risks, validation plan, and open questions prepared for specification.
---

# Notion 할 일 명세 분석

사용자가 명시한 정확한 작업 ID 하나의 내용과 저장소 영향을 분석해 명세화에 필요한 재료를 제공하고 멈춘다.

## 작업 ID 계약

- 현재 요청에 `작업 ID: <정확한 값>`이 반드시 있어야 한다.
- 이전 대화에서 선택한 작업, 제목, 순서, URL, 페이지 UUID를 작업 ID 대신 추론하지 않는다.
- 데이터베이스 스키마에서 작업 식별자 속성을 확인하고 입력값을 exact match한다.
- 결과가 정확히 한 개이고 StoryG Blog relation을 가질 때만 진행한다.
- 누락, 0건, 중복, relation 불일치면 분석하지 않고 정확한 작업 ID를 요청한다.

## 작업 경계

- Notion 페이지, 데이터베이스, 속성, 본문과 저장소를 읽기 전용으로 확인한다.
- 다른 작업을 탐색하거나 대신 선택하지 않는다.
- Notion 상태·속성·본문을 변경하지 않는다.
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
| 저장소 | `/Users/garam/ws/garam/garam-park.github.io` |

## 실행 순서

### 1. 대상 검증

입력한 작업 ID를 exact match해 대상 페이지를 확정한다. 모든 속성과 본문, 필요한 상위·하위·선행·후행 관계를 읽는다. 상태가 `완료`, `취소`, `보관`이면 사용자가 분석을 명시적으로 요청한 경우에만 계속한다.

### 2. 저장소 조사

`AGENTS.md`, 관련 코드·문서·테스트, 최근 이력, 현재 작업 트리 상태를 읽기 전용으로 확인한다. 제목의 단어만으로 범위를 단정하지 말고 `rg`로 실제 관련 경로와 기존 동작을 찾는다.

### 3. 명세 분석

다음 항목을 사실, 추론, 열린 질문으로 구분해 정리한다.

1. 작업 ID, 제목, 상태, Notion 링크
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

### 4. 인계

마지막에 동일한 ID를 포함한 다음 호출을 제공한다.

```text
다음 호출: $notion-specify-task 작업 ID: <정확한 값>
```

## 완료 조건

명시된 한 작업의 명세 분석 보고서와 다음 호출을 제공하면 끝낸다. Notion과 저장소는 실행 전과 동일해야 한다.
