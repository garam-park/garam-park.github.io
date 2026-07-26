---
name: notion-select-task
description: Inspect the current actionable StoryG Blog tasks in the project's Notion task database, compare them, recommend a workable next task, and return its exact database task ID without analyzing its implementation specification or changing anything. Use when the user asks what to work on next, wants a shortlist of current tasks, or invokes the workflow without a task ID. This is the only workflow skill that does not require an explicit task ID.
---

# Notion 할 일 선택

StoryG Blog의 현재 할 일 중 진행할 만한 항목을 비교하고 하나를 추천한 뒤, 후속 스킬에 입력할 정확한 작업 ID를 알려 주고 멈춘다. `$notion-run-queue`가 호출한 경우에는 추천 1순위를 자동 선택한다.

## 작업 경계

- 작업 ID를 입력받지 않는 유일한 단계다.
- Notion 데이터베이스·속성·후보 본문과 저장소 상태를 읽기 전용으로 확인한다.
- 후보의 실행 가능성과 우선순위만 비교하며 상세 명세 분석은 하지 않는다.
- Notion, 파일, branch, worktree, commit, PR, CI, 배포를 변경하지 않는다.
- 사용자가 이미 특정 작업 ID를 제시했다면 선택을 다시 하지 말고 `$notion-analyze-task` 사용을 안내한다.

Notion에는 이 저장소 `.codex/config.toml`의 서버 이름이 정확히 `notion`인 MCP 조회 도구만 사용한다. 노출된 도구 이름이 있다면 `mcp__notion__...`만 허용한다. 다른 Notion 플러그인, `mcp__codex_apps__notion`, 브라우저 자동화, 직접 API 호출로 우회하지 않는다.

## 고정 대상

| 대상 | 값 |
| --- | --- |
| 프로젝트 | `StoryG Blog` |
| 프로젝트 페이지 ID | `3a48e829-7400-81a5-9f3c-cfd701dd3c6c` |
| 할 일 데이터베이스 ID | `3a28e829-7400-808f-b53b-c35b8fef93a8` |
| 현재 data source ID | `3a28e829-7400-80b2-80bf-000bb0ab59ac` |
| 연결 속성 | `프로젝트` |

ID와 스키마를 추측하지 않는다. 데이터베이스를 먼저 읽어 실제 data source, `프로젝트` relation, 사람이 보는 작업 식별자 속성을 확인한다. 작업 식별자는 `unique_id` 유형을 우선하며, 후속 단계에서 exact match할 수 있는 표시값 전체를 `작업 ID`로 사용한다. 식별자 속성을 하나로 정할 수 없으면 후보를 추천하지 말고 문제를 보고한다.

## 실행 순서

### 1. 현재 후보 조회

`프로젝트` relation이 StoryG Blog 페이지를 포함하고 상태가 `일시중단`, `시작 전`, `백로그`인 항목만 조회한다.

- `진행 중`, `주제 검토 요청`, `검토 중`, `완료`, `취소`, `보관`, `모니터링`은 후보에서 제외한다.
- `$notion-run-queue`가 이번 실행에서 이미 처리했거나 `일시중단`으로 보류한 작업 ID도 제외한다.
- 미완료 선행 작업이 있으면 제외하거나 차단됨으로 표시한다.
- 계획용 상위 항목보다 바로 실행 가능한 leaf task를 우선한다.
- relation이나 rollup이 잘렸으면 페이지네이션해 전체를 확인한다.

### 2. 실행 가능성 비교

다음 순서로 판단하되 단순 정렬 결과만으로 확정하지 않는다.

1. `일시중단` → `시작 전` → `백로그`
2. `P0 → P1 → P2 → 미지정`
3. 가까운 마감일
4. 저장소에서 영향 범위를 확인하기 쉬운 작업
5. 외부 결정이나 선행 작업 없이 시작할 수 있는 작업

후보 제목과 핵심 본문, 관련 저장소 위치를 필요한 만큼만 읽는다. 상세 요구사항·완료 조건을 만드는 분석은 다음 스킬에 남긴다.

### 3. 추천과 선택

상위 후보를 작업 ID, 제목, 상태, 우선순위, 추천 이유, 차단 요소와 함께 간결하게 보여 준다. 독립 호출에서는 가장 적합한 하나를 추천하되 후보 간 제품 선택이 필요하면 사용자가 고르게 한다.

`$notion-run-queue`가 호출했으면 위 우선순위와 실행 가능성에 따라 1순위를 자동 선택하고 사용자 응답을 기다리지 않는다. 동점이면 작업 ID의 숫자가 작은 항목을 선택해 결과를 결정적으로 만든다.

선택한 항목을 exact ID로 다시 조회해 한 페이지와 일치하고 StoryG Blog에 연결됐는지 확인한다.

### 4. 인계

선택 결과를 다음 형식으로 끝낸다.

```text
선택한 작업: <제목>
작업 ID: <데이터베이스에 표시된 정확한 값>
Notion 페이지 ID: <UUID>
Notion 링크: <URL>
다음 호출: $notion-analyze-task 작업 ID: <정확한 값>
```

제목, 순번, 페이지 URL만 작업 ID처럼 전달하지 않는다.

## 완료 조건

실행 가능한 후보와 추천 근거를 제시하고, 사용자가 선택한 항목의 정확한 작업 ID를 후속 호출 형식으로 제공하면 끝낸다. 명세 분석과 어떤 변경도 수행하지 않는다.
