---
name: notion-implement-project-task
description: Implement an approved StoryG Blog Notion task specification in an isolated local Git worktree, move the task to in progress, and verify the resulting changes without committing or publishing them. For new or substantially revised posts, also apply the pre-deployment requirements from the Notion document "블로그 검색 최적화 확인 사항"; skip that gate for non-post work. Use when the user asks to start, implement, continue, or finish coding a StoryG Blog TODO whose managed Notion specification has already been approved.
---

# Notion 프로젝트 할 일 구현

확정된 Notion 명세를 기준으로 작업 브랜치에서 구현하고 검증한 뒤, commit 전 상태로 멈춘다.

## 작업 경계

- 대상 TODO와 확정 명세를 다시 확인한다.
- 격리된 branch와 worktree를 준비하거나 기존 작업 공간을 재사용한다.
- Notion `상태`만 `진행 중`으로 변경하고 재조회로 확인한다.
- 명세 범위의 코드·문서·테스트만 수정하고 검증한다.
- Notion 본문과 다른 속성을 변경하지 않는다.
- 파일을 stage하거나 commit, push, PR, merge, CI, 배포 작업을 하지 않는다.
- 기존 worktree, branch, 사용자 변경을 삭제·초기화·덮어쓰지 않는다.

Notion에는 이 저장소 `.codex/config.toml`의 서버 이름이 정확히 `notion`인 MCP만 사용한다. 노출된 도구 이름이 있다면 `mcp__notion__...`만 사용한다. 다른 Notion 플러그인, `mcp__codex_apps__notion`, 브라우저 자동화, 직접 API 호출로 우회하지 않는다. 프로젝트 Notion MCP를 사용할 수 없으면 중단하고 알린다.

## 고정 대상

| 대상 | 값 |
| --- | --- |
| 프로젝트 | `StoryG Blog` |
| 프로젝트 페이지 ID | `3a48e829-7400-81a5-9f3c-cfd701dd3c6c` |
| 할 일 데이터베이스 ID | `3a28e829-7400-808f-b53b-c35b8fef93a8` |
| 현재 data source ID | `3a28e829-7400-80b2-80bf-000bb0ab59ac` |
| 연결 속성 | `프로젝트` |
| 저장소 | `/Users/garam/ws/garam/garam-park.github.io` |
| 기본 통합 branch | `develop` |
| 포스트 Gate 문서 | `블로그 검색 최적화 확인 사항` |
| 포스트 Gate 페이지 ID | `3a88e829-7400-8131-a07a-ee01c056fc8e` |

## 실행 순서

### 1. 사전 조건 확인

대상 TODO를 하나로 식별하고 다음을 모두 확인한다.

1. 할 일 데이터베이스에 속하고 StoryG Blog 프로젝트에 연결됨
2. 본문에 `## Codex 구현 명세`와 marker ``notion-specify-project-task/v1``가 정확히 하나 있음
3. 명세에 목표, 요구사항, 완료 조건, 검증 계획이 있음
4. 구현 방향을 바꾸는 열린 질문이 남아 있지 않음
5. 미완료 선행 작업이 없음
6. 상태가 `백로그`, `시작 전`, `일시중단`, `진행 중` 중 하나임

marker는 `$notion-specify-project-task`가 사용자 승인 뒤 저장한 명세임을 뜻한다. marker가 없거나 중복됐으면 구현하지 않고 명세화 단계로 돌려보낸다. `완료`, `취소`, `보관` 작업은 명시적인 재개 승인 없이는 구현하지 않는다.

### 2. 기존 작업 흔적 확인

저장소의 `AGENTS.md`, `git status --short`, `git worktree list`, local·remote branch를 확인한다. TODO 번호가 같은 기존 branch나 worktree가 있으면 새로 만들지 말고 내용을 검토해 안전하게 재사용한다.

- branch: `codex/todo-<번호>-<짧은-slug>`
- worktree: 저장소 루트의 `.worktrees/todo-<번호>`

기존 경로가 다른 작업에 사용 중이거나 branch와 worktree 관계가 불명확하면 변경하지 말고 사용자에게 알린다. 기존 branch를 reset, rebase, rename, delete하지 않는다.

기존 작업 흔적이 없으면 사용자가 지정한 기준 branch를 사용한다. 지정이 없으면 이 저장소의 통합 branch인 `develop`을 기준으로 branch와 worktree를 만든다. 기준 branch의 최신성을 확인하되 사용자의 기본 worktree 변경에는 손대지 않는다.

### 3. 작업 시작 기록

worktree 준비가 끝난 뒤에만 Notion `상태`를 `진행 중`으로 변경한다. 이미 `진행 중`이면 중복 갱신하지 않는다. 갱신 뒤 페이지를 다시 읽어 실제 상태를 확인한다.

상태 변경이나 검증에 실패하면 제품 파일을 수정하기 전에 멈춘다.

### 4. 포스트 작업 조건부 Gate

다음 중 하나면 포스트 작업으로 본다.

- `_posts/**` 또는 `_draft/**`에 새 글을 추가함
- 기존 글의 기술 내용, 명령, 버전, 구성, 결론, 메타데이터를 실질적으로 개편함
- Notion 명세가 새 포스트 작성, 포스트 개편, 검색 최적화를 명시함

오탈자·띄어쓰기·링크 한 건 같은 경미한 교정이나 코드·템플릿·인프라 작업이면 포스트 Gate를 생략하고 완료 보고에 이유를 남긴다.

포스트 작업이면 프로젝트 Notion MCP로 Gate 페이지를 최신 상태로 읽는다. 읽을 수 없으면 기준을 추측하거나 오래된 기억으로 구현하지 말고 중단한다.

구현 중 다음 범위를 체크리스트로 함께 적용한다.

- 2장 작성 전 브리프
- 3장 front matter와 메타데이터
- 4장 본문 품질
- 5장 AI 검색 친화성
- 6장 Google 전용 배포 Gate 중 source·local build에서 확인 가능한 항목
- 7장 Naver 전용 배포 Gate 중 source·local build에서 확인 가능한 항목

대표 이미지가 없으면 이미지 전용 항목은 조건부 제외한다. 운영 HTTP 200, Search Console, 서치어드바이저처럼 배포 뒤에만 확인 가능한 항목은 `배포 후 확인 대기`로 남긴다. 9장 플랫폼 정비 항목은 현재 명세에 포함되지 않으면 구현 범위를 자동으로 넓히지 않고 후속 과제로 보고한다.

확인 가능한 공통·Google·Naver Gate가 미통과이면 구현 완료로 보고하지 않는다.

### 5. 명세 구현

격리된 worktree 안에서만 작업한다.

1. 명세의 완료 조건을 구현 체크리스트로 사용한다.
2. `rg`로 실제 영향 지점을 확인한 뒤 필요한 최소 파일만 수정한다.
3. 기존 구조와 스타일을 따른다.
4. 동작 변경에는 적절한 테스트 또는 검증 수단을 추가한다.
5. 명세 밖 리팩터링과 사용자 변경을 섞지 않는다.
6. 중요한 명세 충돌이나 범위 확대가 발견되면 구현을 멈추고 사용자에게 결정 근거를 제시한다.

파일 수정에는 `apply_patch`를 사용한다. 새 의존성이나 외부 시스템 변경이 필요하면 자동으로 범위를 넓히지 않는다.

### 6. 검증

변경 위험에 비례해 다음을 수행한다.

1. 가장 가까운 단위 검증
2. 관련 lint·format·정적 검사
3. 필요한 경우 프로젝트 build
4. `git diff --check`
5. `git status --short`와 diff 전체 검토
6. 명세의 각 완료 조건 충족 여부 확인
7. 포스트 작업이면 공통·Google·Naver Gate 판정과 배포 후 확인 대기 항목 정리

검증 명령을 실행할 수 없으면 이유와 미검증 범위를 명시한다. 실패를 숨기거나 완료로 보고하지 않는다.

## 중복 실행과 재개

- 실행 키는 TODO 번호와 작업 branch다.
- 기존 worktree에 변경이 있으면 이전 구현으로 간주해 먼저 diff와 상태를 분석한다.
- 같은 Notion 상태, branch, worktree를 다시 만들거나 갱신하지 않는다.
- 중단 시 branch와 worktree를 보존하고 실패한 검증 또는 미완료 조건부터 재개한다.
- 재개할 때 Notion 명세를 다시 읽는다. 기존 구현과 충돌하는 실질적 명세 변경이 있으면 자동 수정하지 말고 알린다.
- 실패했다고 worktree나 branch를 삭제하거나 변경을 되돌리지 않는다.

## 완료 조건

다음을 모두 만족하면 끝낸다.

- Notion 상태가 `진행 중`
- 작업 branch와 격리 worktree가 하나씩 존재
- 구현 diff가 확정 명세 범위 안에 있음
- 가능한 검증이 통과하고 미검증 항목이 명시됨
- 포스트 작업이면 확인 가능한 검색 최적화 Gate가 통과 또는 조건부 통과하고, 비포스트 작업이면 생략 이유가 기록됨
- 변경 파일, 검증 결과, 남은 위험이 사용자에게 보고됨

파일은 stage하지 않은 상태로 남긴다. commit·push·PR 생성은 다음 단계 스킬에 맡긴다.
