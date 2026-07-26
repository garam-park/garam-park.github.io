---
name: notion-analyze-project-task
description: Read, select, and analyze StoryG Blog tasks linked through the project's Notion task database without changing anything. Use when the user asks to inspect available StoryG Blog work, choose the next task, analyze a TODO item or Notion task URL, explain its purpose and likely repository impact, or identify questions before specification or implementation.
---

# Notion 프로젝트 할 일 분석

StoryG Blog에 연결된 할 일을 확인하고 하나를 선택해 분석한 뒤 멈춘다.

## 작업 경계

읽기 전용으로 실행한다.

- Notion 페이지, 데이터베이스, 속성, 본문을 조회한다.
- 저장소의 파일, 이력, 현재 변경 상태를 조회한다.
- Notion 상태·속성·본문을 변경하지 않는다.
- 파일 수정, 브랜치·worktree 생성, commit, push, PR 생성·수정, CI·배포 실행을 하지 않는다.
- 명세를 확정하거나 구현을 시작하지 않는다.

Notion에는 이 저장소 `.codex/config.toml`의 서버 이름이 정확히 `notion`인 MCP만 사용한다. 노출된 도구 이름이 있다면 `mcp__notion__...`의 조회 도구만 사용한다. 다른 Notion 플러그인, `mcp__codex_apps__notion`, 브라우저 자동화, 직접 API 호출로 우회하지 않는다. 프로젝트 Notion MCP를 사용할 수 없으면 중단하고 알린다.

## 고정 대상

| 대상 | 값 |
| --- | --- |
| 프로젝트 | `StoryG Blog` |
| 프로젝트 페이지 ID | `3a48e829-7400-81a5-9f3c-cfd701dd3c6c` |
| 할 일 데이터베이스 ID | `3a28e829-7400-808f-b53b-c35b8fef93a8` |
| 현재 data source ID | `3a28e829-7400-80b2-80bf-000bb0ab59ac` |
| 연결 속성 | `프로젝트` |
| 저장소 | `/Users/garam/ws/garam/garam-park.github.io` |

ID를 추측하지 않는다. 데이터베이스를 먼저 조회해 실제 data source와 스키마를 확인한다. `프로젝트`가 relation인지, 대상 프로젝트 페이지가 실제로 `StoryG Blog`인지 검증한다. 구조가 달라 의미를 하나로 식별할 수 없을 때만 사용자에게 묻는다.

## 실행 순서

### 1. 할 일 조회

할 일 data source에서 `프로젝트` relation이 StoryG Blog 페이지 ID를 포함하는 항목만 조회한다. 사용자가 TODO ID나 페이지 URL을 지정했으면 해당 항목이 이 결과에 속하는지 확인한다.

사용자가 특정 항목을 지정하지 않았으면 다음 순서로 선택한다.

1. `진행 중` 항목을 우선한다.
2. 진행 중 항목이 없으면 `시작 전`, `백로그` 순서로 본다.
3. 완료되지 않은 선행 작업이 있는 항목은 제외한다.
4. 계획용 상위 항목보다 실행 가능한 하위 없는 항목을 우선한다.
5. 같은 단계에서는 `P0 → P1 → P2 → 미지정`, 마감일, TODO 번호 순서로 고른다.
6. 서로 다른 `진행 중` 항목이 둘 이상이면 임의 선택하지 말고 후보와 차이를 보여 주고 사용자 선택을 기다린다.

`일시중단`, `완료`, `취소`, `보관` 항목은 사용자가 명시하지 않으면 선택하지 않는다.

### 2. 내용 확인

선택한 작업의 모든 속성과 본문을 읽는다. 상위·하위 항목, 선행·후행 작업이 있으면 분석에 필요한 관계 페이지도 읽는다. 관계 속성이 페이지 크기 때문에 잘렸으면 해당 property를 페이지네이션해 확인한다.

저장소에서는 `AGENTS.md`, 관련 파일, 최근 이력, 현재 작업 트리 상태를 읽기 전용으로 확인한다. 제목의 단어만으로 영향 범위를 단정하지 말고 `rg`로 실제 관련 코드를 찾는다.

### 3. 분석 보고

다음 순서로 간결하게 보고한다.

1. 선택한 할 일: TODO ID, 제목, 상태, Notion 링크
2. 선택 근거
3. 목적과 배경
4. 예상 범위와 비범위
5. 영향 가능성이 있는 저장소 파일
6. 의존성, 위험, 불명확한 점
7. 다음 단계에서 명세해야 할 항목

Notion이나 저장소에서 확인한 사실과 분석상 추론을 구분한다. 정보가 부족하면 추측으로 채우지 말고 열린 질문으로 남긴다.

## 완료 조건

분석 보고서를 제공하면 끝낸다. Notion과 저장소가 실행 전과 동일한지 확인하고, 다음 단계로 명세화를 제안할 수는 있지만 수행하지 않는다.
