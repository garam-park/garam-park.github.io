---
name: notion-create-pr
description: >-
  Publish the implemented work for exactly one StoryG Blog Notion task identified by an explicit exact task ID by validating its isolated worktree, committing only that task's changes, pushing its branch, creating or reusing a draft pull request, and recording the links in the same Notion task. Use when the user supplies `작업 ID: ID값` and asks to push or create a PR for that implemented task.
---

# Notion 프로젝트 PR 생성

검증된 구현 결과를 commit·push하고 draft PR을 만든 뒤 Notion 할 일에 연결 정보를 기록하고 멈춘다.

## 작업 ID 계약

- 현재 요청에 `작업 ID: <정확한 값>`이 반드시 있어야 한다.
- 제목, branch, worktree, 이전 대화만으로 작업 ID를 추론하지 않는다.
- 입력 ID를 데이터베이스에 exact match하고 TODO, 명세, branch, worktree가 같은 ID를 가리키는지 확인한다.
- ID가 누락되거나 연결이 다르면 stage, commit, push, PR, Notion 쓰기를 하지 않는다.

## 작업 경계

- 확정 명세, 구현 diff, 검증 결과를 다시 확인한다.
- 해당 TODO의 변경만 stage하고 의도적인 commit을 만든다.
- 작업 branch를 force 없이 push한다.
- 동일 branch의 기존 PR을 재사용하거나 draft PR을 하나만 만든다.
- Notion 본문의 연결 관리 구역만 갱신한다.
- 리뷰 수정, merge, 배포, Notion 완료 처리를 하지 않는다.
- 사용자의 다른 변경, branch, worktree, commit을 수정하거나 삭제하지 않는다.

정확한 작업 ID를 포함해 이 스킬을 실행해 달라는 요청은 해당 변경의 commit·push·draft PR 생성과 Notion 연결 기록을 승인한 것으로 본다. 예상하지 못한 파일이나 범위 밖 변경이 있으면 자동으로 포함하지 말고 사용자에게 확인한다.

Notion에는 이 저장소 `.codex/config.toml`의 서버 이름이 정확히 `notion`인 MCP만 사용한다. 노출된 도구 이름이 있다면 `mcp__notion__...`만 사용한다. 다른 Notion 플러그인, `mcp__codex_apps__notion`, 브라우저 자동화, 직접 API 호출로 우회하지 않는다.

GitHub에는 연결된 GitHub 도구를 우선 사용하고, 필요한 기능이 없을 때만 `gh`를 사용한다. 인증 정보나 secret을 읽거나 출력하지 않는다.

## 고정 대상

| 대상 | 값 |
| --- | --- |
| 프로젝트 | `StoryG Blog` |
| 프로젝트 페이지 ID | `3a48e829-7400-81a5-9f3c-cfd701dd3c6c` |
| 할 일 데이터베이스 ID | `3a28e829-7400-808f-b53b-c35b8fef93a8` |
| 현재 data source ID | `3a28e829-7400-80b2-80bf-000bb0ab59ac` |
| GitHub 저장소 | `garam-park/garam-park.github.io` |
| 기본 PR 대상 branch | `develop` |

## 실행 순서

### 1. 대상과 사전 조건 확인

입력한 작업 ID로 대상 TODO, 작업 branch, worktree를 하나로 식별하고 다음을 확인한다.

1. TODO가 StoryG Blog에 연결되고 상태가 `진행 중`임
2. 본문에 확정 명세 marker ``notion-specify-project-task/v1``가 정확히 하나 있음
3. branch 이름이 `codex/todo-<번호>-<slug>` 형식이고 해당 TODO와 일치함
4. worktree의 변경이 확정 명세 범위 안에 있음
5. 구현 단계에서 약속한 검증이 통과했거나 미검증 사유가 명확함
6. merge conflict, 범위 밖 변경, secret, 대용량 생성물이 없음

사용자가 PR 대상 branch를 지정하면 그 값을 사용한다. 지정이 없으면 구현 branch의 기준 branch를 확인하고, 식별할 수 없을 때만 이 저장소 기본값 `develop`을 사용한다.

### 2. 중복과 원격 상태 확인

commit이나 push 전에 다음을 읽기 전용으로 확인한다.

- local·remote branch와 ahead/behind 상태
- 같은 head branch의 open, closed, merged PR
- 기록된 Notion 연결 관리 구역

open PR이 이미 있으면 새 PR을 만들지 않고 재사용한다. closed 또는 merged PR이 있으면 새 PR을 자동 생성하지 말고 상태를 보고한다. remote branch가 예상하지 못하게 갈라졌으면 force push하지 말고 멈춘다.

### 3. 최종 검증과 commit

작업 worktree에서 관련 테스트, build, `git diff --check`, `git status --short`, base branch 대비 diff를 다시 확인한다.

변경 파일을 하나씩 검토하고 해당 TODO에 속하는 경로만 명시적으로 stage한다. `git add -A`처럼 범위가 넓은 명령을 사용하지 않는다. stage 뒤 cached diff와 파일 목록을 다시 확인한다.

commit 메시지는 변경 성격과 TODO 제목을 반영해 간결하게 작성한다. AI 관련 trailer, 서명, footer를 추가하지 않는다. 기존 commit을 amend, squash, rebase하지 않는다.

이미 적절한 commit이 있고 worktree가 깨끗하면 중복 commit을 만들지 않는다.

### 4. push와 draft PR

작업 branch만 origin에 push하고 upstream을 설정한다. force push하지 않는다.

PR을 만들기 직전에 같은 head branch의 PR을 다시 조회한다. 없을 때만 draft PR을 생성한다.

PR 생성 요청이 오류나 timeout으로 끝나면 바로 다시 생성하지 않는다. `repo + head branch + base branch`로 다시 조회해 PR이 실제로 생겼는지 확인하고, 하나가 확인되면 그 PR을 성공 결과로 재사용한다.

PR 제목은 `[TODO-<번호>] <할 일 제목>` 형식을 기본으로 하고, 본문에는 다음을 포함한다.

- Notion TODO 링크
- 배경과 목표 요약
- 주요 변경
- 비범위
- 검증 결과와 미검증 항목
- 위험과 리뷰 포인트
- head SHA와 base branch

PR의 head, base, draft 여부, URL을 재조회해 확인한다.

### 5. 초기 CI 확인

PR 생성 직후 최신 head SHA에 연결된 check가 나타나는지 확인한다. 이미 결과가 있으면 run URL과 상태를 수집한다. check가 아직 시작되지 않았으면 `pending`으로 기록한다.

CI 완료를 오래 기다리거나 실패를 수정하지 않는다. 이 단계의 책임은 PR과 초기 상태를 연결하는 데까지다.

### 6. Notion 연결 기록

외부 작업이 성공한 뒤 대상 TODO의 최신 본문을 다시 읽고 아래 관리 구역을 본문 끝에 한 번만 추가하거나 정확히 교체한다.

```markdown
## Codex 구현 연결

`notion-create-project-pr/v1`

- 작업 ID: `TODO-<번호>`
- 기준 branch: `develop`
- 작업 branch: `codex/todo-<번호>-<slug>`
- head commit: `<sha>`
- draft PR: <PR URL>
- CI: `<pending|success|failure>` <run URL>
```

- marker가 없으면 한 번만 추가한다.
- marker가 하나면 해당 관리 구역만 교체한다.
- marker가 둘 이상이면 쓰지 말고 중복을 보고한다.
- 작업 ID 필드가 없는 기존 v1 기록은 대상 페이지의 exact ID, branch, PR 본문의 Notion 링크가 모두 일치할 때만 legacy 연결로 인정하고 다음 정상 갱신 때 작업 ID를 추가한다.
- 확정 명세와 사용자 작성 영역을 덮어쓰거나 정리하지 않는다.
- Notion 상태와 속성은 변경하지 않는다.

갱신 뒤 본문을 재조회해 작업 ID, branch, SHA, PR URL, CI 상태가 실제 외부 상태와 일치하는지 확인한다.

## 중단과 재개

- push가 성공하고 PR 생성이 실패했으면 기존 remote branch에서 재개한다.
- PR 생성 뒤 Notion 갱신이 실패했으면 기존 PR을 재사용하고 Notion 기록만 재시도한다.
- 동일 SHA의 commit, push, PR을 반복하지 않는다.
- 부분 성공을 되돌리거나 branch·PR을 삭제하지 않는다.
- 실패 지점과 이미 성공한 외부 작업의 URL·SHA를 보고한다.

## 완료 조건

다음을 모두 만족하면 끝낸다.

- task 변경이 commit되어 worktree가 깨끗함
- remote 작업 branch가 local head SHA와 일치함
- 올바른 head·base의 draft PR이 하나 존재함
- 초기 CI 상태가 확인됨
- Notion 연결 관리 구역이 정확한 작업 ID와 실제 branch, SHA, PR, CI 정보를 가리킴

리뷰 대응, CI 수정, merge, 배포는 다음 단계 스킬에 맡긴다.

```text
다음 호출: $notion-review-pr 작업 ID: <정확한 값> PR: <PR URL>
```
