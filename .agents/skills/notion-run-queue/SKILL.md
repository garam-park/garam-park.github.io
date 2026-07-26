---
name: notion-run-queue
description: Automatically process the StoryG Blog Notion task queue one task at a time from selection through analysis, specification drafting, multi-agent specification approval, isolated implementation, draft PR creation, multi-agent PR review and fixes, and final human review request. Use when the user wants all actionable tasks in 일시중단, 시작 전, and 백로그 handled repeatedly until no eligible task remains. Route meaningless or product-decision-blocked tasks to 주제 검토 요청, defer repeated transient failures to 일시중단, and never merge or deploy.
---

# Notion 자동 작업 큐

StoryG Blog의 실행 가능한 작업을 하나씩 골라 사람 검토 요청까지 처리하고, 후보가 없어질 때까지 반복한다.

## 호출 권한과 절대 경계

사용자가 이 스킬을 호출하면 각 작업에 정확한 ID를 전달해 다음 하위 스킬을 연속 실행하는 것을 승인한 것으로 본다.

1. `$notion-select-task`
2. `$notion-analyze-task`
3. `$notion-specify-task`
4. `$notion-review-spec`
5. `$notion-implement-task`
6. `$notion-create-pr`
7. `$notion-review-pr`
8. `$notion-request-review`

필요하면 `$notion-request-topic-review`로 인계한다.

이 권한에는 관리 명세·상태·담당자·댓글 갱신, 격리 worktree의 구현, 검증, 해당 작업의 commit, 일반 push, draft PR 생성과 갱신, 리뷰 수정 commit, draft 해제, 사람 검토 요청이 포함된다. 실제 GitHub merge, `main` 변경, 배포, 운영 URL 검사, Notion `완료` 처리는 포함되지 않는다.

다음도 하지 않는다.

- force push, amend, rebase, branch·worktree·PR 삭제
- 관련 없는 사용자 변경 포함·수정·초기화
- 사람 대신 GitHub approval
- 제품 결정을 추측해 명세 확정

Notion에는 프로젝트 `.codex/config.toml`의 이름이 정확히 `notion`인 MCP만 사용한다. 노출된 도구 이름이 있다면 `mcp__notion__...`만 허용한다. 다른 Notion 플러그인, 브라우저 자동화, 직접 API 호출로 우회하지 않는다.

## 큐 상태

실행 중 다음 집합을 유지한다.

- `completed_this_run`: `$notion-request-review`까지 끝난 작업 ID
- `topic_review_this_run`: `$notion-request-topic-review`로 넘긴 작업 ID
- `deferred_this_run`: 반복된 기술 실패로 `일시중단`한 작업 ID
- `active_task`: 현재 처리 중인 작업 ID, Notion 페이지 ID, 단계, branch, worktree, PR, latest head SHA

한 번에 `active_task`는 하나만 둔다. 모든 단계에 정확한 `작업 ID`를 명시해 전달하고 제목이나 URL로 대신하지 않는다.

## 선택 규칙

매 반복 시작에 `$notion-select-task`를 자동 큐 모드로 실행한다.

- 후보 상태는 `일시중단`, `시작 전`, `백로그`만 허용한다.
- `진행 중`은 완전히 제외한다. 이전 자동 실행이 중단된 흔적이 있어도 새 실행에서 자동 재개하지 않는다.
- `주제 검토 요청`, `검토 중`, `완료`, `취소`, `보관`, `모니터링`도 제외한다.
- 이번 실행의 세 집합에 든 ID를 제외한다.
- 후보가 있으면 추천 1순위를 사용자 확인 없이 선택한다.
- 후보가 없으면 정상 종료한다.

## 작업별 상태 기계

선택한 ID를 exact match한 뒤 Notion 본문·속성과 Git branch·worktree·PR을 연결해 현재 단계를 판단한다. 증거가 완전한 완료 단계만 건너뛴다.

1. `$notion-analyze-task`: 읽기 전용 분석을 항상 새로 만들어 이후 단계에 같은 ID로 전달
2. `$notion-specify-task`: 확정 관리 명세가 없으면 검토 초안을 저장
3. `$notion-review-spec`: 초안이면 멀티에이전트 검토·수정을 반복해 자동 확정
4. `$notion-implement-task`: 확정 명세면 worktree에서 구현하고 `진행 중` 및 시작 댓글 기록
5. `$notion-create-pr`: 구현이 검증됐으면 해당 변경만 commit·push하고 draft PR 연결
6. `$notion-review-pr`: 최신 PR이 승인 가능해질 때까지 독립 reviewer와 단일 fixer를 반복
7. `$notion-request-review`: latest head와 CI를 재검증해 garam에게 배정, `검토 중`, 실제 mention 댓글 기록

이미 존재하는 명세, worktree, branch, commit, PR, reviewer 기록은 각 하위 스킬의 재개 규칙으로 검증해 재사용한다. 단계 증거가 일부만 있거나 서로 다르면 앞선 안전한 단계에서 복구하며 중복 외부 작업을 만들지 않는다.

`$notion-implement-task`가 상태를 `진행 중`으로 바꾼 뒤에도 현재 실행의 `active_task`는 계속 처리한다. 단, 큐를 새로 시작할 때 `진행 중` 작업을 다시 선택하지 않는다.

## 주제 검토 분기

분석 또는 명세 리뷰에서 다음이 근거로 확인되면 구현하지 않고 `$notion-request-topic-review`를 호출한다.

- 작업이 무의미하거나 StoryG Blog 목표와 무관함
- 서로 모순된 요구 때문에 결과를 정할 수 없음
- 제품·주제 선택 없이는 검증 가능한 명세를 만들 수 없음
- 선행 결정이 없어 현재 형태로 진행할 가치가 없음

정확한 작업 ID, 구체적인 사유, 사람이 결정할 확인 필요를 전달한다. 인계가 검증되면 ID를 `topic_review_this_run`에 넣고 다음 후보로 이동한다.

## 기술 실패와 재시도

Notion·GitHub·CI·network·tool 오류, flaky test, rate limit은 주제 검토 사유가 아니다.

- 같은 작업의 같은 단계는 최초 시도 뒤 최대 2회만 재시도한다.
- 재시도 전 이미 성공한 상태를 재조회해 성공한 쓰기·commit·push·PR을 반복하지 않는다.
- 세 번째 실패 뒤 대상 상태를 안전하게 변경할 수 있으면 `일시중단`으로 바꾸고, 실패 단계·증거·재개 지점을 marker ``[codex-task-paused/v1]`` 댓글로 한 번 기록한다.
- 해당 ID를 `deferred_this_run`에 넣고 다음 후보로 이동한다.
- 이미 `진행 중`인 작업의 상태나 댓글을 바꿀 수 없으면 현재 흔적을 보존하고 ID만 이번 실행에서 보류한 뒤 보고한다.

Notion 또는 GitHub가 모든 후보에 공통으로 필요한데 서비스 전체 장애나 권한 문제로 사용할 수 없음이 확인된 경우에만 전체 큐를 중단한다. 한 작업의 실패나 CI 실패만으로 전체 큐를 중단하지 않는다.

## 반복과 종료

각 작업이 `$notion-request-review`까지 완료되면 `completed_this_run`에 넣고 `active_task`를 비운 뒤 다시 선택한다. 고정 작업 수 제한이나 busy wait를 두지 않는다.

다음 중 하나로 끝낸다.

- 정상 종료: 제외 집합을 적용한 뒤 `일시중단`, `시작 전`, `백로그` 후보가 없음
- 전역 중단: 프로젝트 Notion MCP 또는 GitHub 접근의 전역 장애로 어떤 후보도 안전하게 처리할 수 없음

최종 보고에는 작업 ID별로 `검토 요청 완료`, `주제 검토 요청`, `일시중단`을 구분하고 PR URL·latest head·실패 재개 지점을 포함한다. merge나 배포가 수행되지 않았음을 명시한다.
