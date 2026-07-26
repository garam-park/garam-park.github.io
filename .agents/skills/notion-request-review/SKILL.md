---
name: notion-request-review
description: Request human review for exactly one approval-ready StoryG Blog pull request identified by an explicit exact Notion task ID and PR. Revalidate the latest PR head, CI, review-ready record, task linkage, schema, and garam user; then assign the Notion task to garam, move its exact status to 검토 중, and add one real user-mention comment asking 검토해주세요. Use after notion-review-pr reports approval-ready quality, or to safely resume a partially completed review-request handoff. Do not merge, deploy, or complete the task.
---

# Notion 검토 요청

승인 가능한 최신 PR을 사람 검토 단계로 인계한다. 대상 Notion 할 일의 담당자를 `garam`으로 지정하고 상태를 `검토 중`으로 바꾼 뒤, 실제 사용자 멘션이 포함된 `검토해주세요` 댓글을 한 번만 남긴다.

## 작업 ID 계약

- 현재 요청에 `작업 ID: <정확한 값>`과 기존 PR 번호 또는 URL이 반드시 있어야 한다.
- 이전 대화, 제목, branch, PR만으로 작업 ID를 추론하지 않는다.
- 입력 ID를 데이터베이스의 `ID` unique_id에 exact match한다.
- 대상 페이지, 확정 명세, PR 연결 기록, branch가 모두 같은 작업 ID를 가리켜야 한다.
- 누락, 0건, 중복, 연결 불일치면 아무것도 변경하지 않는다.

## 권한과 경계

정확한 작업 ID와 PR을 포함해 이 스킬을 실행해 달라는 요청은 다음 세 가지 Notion 변경만 승인한 것으로 본다.

1. `담당자`를 `garam`으로 지정
2. `상태`를 `검토 중`으로 변경
3. `garam` 실제 사용자 멘션 뒤에 `검토해주세요`라고 페이지 댓글 작성

다음은 하지 않는다.

- 코드, branch, commit, PR, review, CI 변경
- Notion 본문이나 다른 속성 변경
- GitHub approval, merge, 배포, Notion 완료 처리
- 다른 담당자 제거, 댓글 중복 작성

Notion에는 이 저장소 `.codex/config.toml`의 이름이 정확히 `notion`인 MCP만 사용한다. 노출된 도구 이름이 있다면 `mcp__notion__...`만 허용한다. 다른 Notion 플러그인, `mcp__codex_apps__notion`, 브라우저 자동화, 직접 API 호출로 우회하지 않는다.

GitHub에는 연결된 GitHub 도구를 우선 사용하고 필요한 조회 기능이 없을 때만 `gh`를 사용한다. secret이나 인증 정보를 읽거나 출력하지 않는다.

## 확인된 대상

실행할 때 아래 값을 프로젝트 Notion MCP로 다시 읽어 일치 여부를 확인한다.

| 대상 | 값 |
| --- | --- |
| 프로젝트 | `StoryG Blog` |
| 프로젝트 페이지 ID | `3a48e829-7400-81a5-9f3c-cfd701dd3c6c` |
| 할 일 data source ID | `3a28e829-7400-80b2-80bf-000bb0ab59ac` |
| 작업 ID 속성 | `ID` (`unique_id`, prefix `TODO`) |
| 담당자 속성 | `담당자` (`people`) |
| 검토 상태 | `검토 중` |
| 검토자 이름 | `garam` |
| 검토자 user ID | `a0ffaf82-2f8c-4df5-ad5f-9c38a03a453a` |

이름만 보고 다른 사용자를 선택하지 않는다. user ID가 없거나 이름·유형이 `garam`·`person`과 다르면 변경하지 않는다.

## 실행 순서

### 1. 최신 대상 확인

작업 ID로 대상 페이지를 exact match하고 다음을 확인한다.

1. StoryG Blog relation을 가짐
2. 상태가 `진행 중` 또는 이미 `검토 중`임
3. 확정 명세 marker ``notion-specify-project-task/v1``가 하나 있음
4. PR 연결 marker ``notion-create-project-pr/v1``가 하나 있음
5. 연결 기록의 작업 ID, branch, PR, head SHA가 입력 대상과 일치함

`완료`, `취소`, `보관`, `모니터링` 상태에서는 자동으로 되돌리지 않는다.

### 2. 승인 가능 상태 재검증

Notion 기록만 신뢰하지 말고 최신 GitHub 상태를 읽는다.

- PR이 open이고 merge되지 않음
- PR head가 Notion에 기록된 head SHA와 일치함
- PR이 draft가 아님
- 최신 head의 필수 CI가 모두 성공함
- unresolved actionable review thread가 없음
- Notion 연결 관리 구역에 `review: 승인 가능`이 기록됨
- 포스트 작업의 배포 전 Gate가 통과 또는 조건부 통과함

head, base, CI, review thread 중 하나라도 바뀌었거나 확인할 수 없으면 Notion을 변경하지 않고 `$notion-review-pr`로 돌려보낸다.

### 3. 스키마·사용자·중복 확인

쓰기 직전에 data source, 대상 페이지, 전체 사용자 목록, 기존 페이지 댓글을 다시 읽는다.

- `담당자`가 people이고 `상태`에 정확히 `검토 중` 옵션이 있는지 확인한다.
- 예상 user ID가 `garam` person인지 확인한다.
- 담당자가 비어 있거나 `garam`만 있으면 계속한다.
- 다른 담당자가 있으면 자동 제거하거나 교체하지 말고 사용자에게 확인한다.
- 기존 댓글에 marker ``[codex-review-request/v1]``, 같은 작업 ID·PR·latest head, garam user ID의 실제 mention, `검토해주세요` 문구가 모두 있으면 현재 head의 댓글 완료로 본다.

표시 문자열 `@garam`만 있는 댓글은 실제 멘션으로 간주하지 않는다.

marker가 없는 기존 mention 댓글은 댓글 생성 시각이 현재 approval-ready 연결 기록보다 늦고 그 뒤 PR head가 바뀌지 않았을 때만 legacy 완료로 인정한다.

### 4. 속성 갱신

하나의 page property update로 다음 값을 함께 적용한다.

- `담당자.people`: garam user ID 한 명
- `상태.status.name`: `검토 중`

이미 같은 값이면 중복 쓰지 않는다. 갱신 뒤 페이지를 재조회해 두 속성을 확인한다. 둘 중 하나라도 다르면 댓글을 쓰지 말고 실제 상태와 재개 지점을 보고한다.

### 5. 멘션 댓글 작성

동일 실행 키의 댓글이 없을 때만 페이지 수준 댓글을 rich text로 작성한다.

```text
[codex-review-request/v1]

작업 ID: TODO-123
PR: <PR URL>
head: <latest SHA>
CI: success

@garam 검토해주세요
다음 행동: 승인 또는 수정 요청
```

`@garam` 부분은 문자열이 아니라 user ID `a0ffaf82-2f8c-4df5-ad5f-9c38a03a453a`를 가리키는 실제 `user` mention rich text로 작성한다.

댓글 작성 뒤 marker, 작업 ID, PR, latest head, mention user ID, 문구를 다시 읽어 확인한다. 단순 텍스트 `@garam 검토해주세요`로 대체하지 않는다.

## 중복 실행과 재개

- 실행 키는 정확한 작업 ID, PR 번호, latest head SHA, garam user ID다.
- 속성 갱신 뒤 댓글 작성이 실패하면 속성을 되돌리지 않고 댓글 단계부터 재개한다.
- 이미 속성과 댓글이 모두 일치하면 쓰기 없이 완료로 보고한다.
- 동일 실행 키의 mention 댓글을 두 번 만들지 않는다.
- PR head가 바뀌면 이전 승인 가능 판정과 이전 댓글 키를 폐기하고 리뷰 단계로 돌아간다. 새 head가 다시 승인 가능해지면 새 실행 키로 한 번 알린다.

## 완료 조건

다음을 재조회로 모두 확인하면 끝낸다.

- 대상 작업 ID와 PR 연결이 최신 상태임
- 담당자에 `garam`만 있음
- 상태가 정확히 `검토 중`임
- 현재 작업 ID, PR, latest head에 결속된 marker 댓글에 실제 garam user mention과 `검토해주세요`가 있음

merge, 배포, Notion 완료 처리는 별도 단계에 맡긴다.
