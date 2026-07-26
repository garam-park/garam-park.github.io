---
name: notion-run-queue
description: >-
  Automatically resume specification-stage StoryG Blog Notion tasks, then process new tasks one at a time through analysis, specification drafting, multi-agent specification approval, isolated implementation, draft PR creation, multi-agent PR review and fixes, and final human review request. Use when the user wants every actionable task in 명세, 일시중단, 시작 전, and 백로그 handled until no automatic candidate remains. Route product-decision-blocked tasks to 주제 검토 요청, defer repeated technical failures to 일시중단, and never merge or deploy.
---

# Notion 자동 작업 큐

StoryG Blog의 중단된 명세 작업을 먼저 재개하고 새 작업을 하나씩 사람 검토 요청까지 처리한다.

## 사전 조건과 단일 실행

실행 전에 프로젝트 Notion MCP로 data source를 읽어 다음을 확인한다.

- `상태`가 status 유형임
- `명세`, `일시중단`, `시작 전`, `백로그`, `진행 중`, `주제 검토 요청`, `검토 중` 옵션이 정확히 존재함
- StoryG Blog relation과 `ID` unique_id를 식별할 수 있음

`명세` 옵션이 없으면 어떤 작업도 변경하지 않고 옵션 생성을 요청한다.

동일 프로젝트에서는 `$notion-run-queue`를 한 번에 하나만 실행한다. Notion 상태와 댓글의 read-then-write는 atomic lock이 아니므로 동시에 두 큐를 실행하거나 mutating 하위 스킬을 병행하지 않는다.

첫 외부 쓰기 전에 이 스킬의 `scripts/queue_lease.py`로 Git common directory의 atomic local lease를 얻는다.

```text
python3 .agents/skills/notion-run-queue/scripts/queue_lease.py acquire \
  --repo /Users/garam/ws/garam/garam-park.github.io \
  --run-id queue-<KST timestamp>-<random>
```

- 종료 또는 전역 중단 시 같은 run ID로 `release`한다.
- 다른 owner가 있거나 owner record가 깨졌으면 자동으로 지우거나 탈취하지 않고 중단해 owner 정보를 보고한다.
- 프로세스 비정상 종료로 lease가 남으면 `status`로 owner를 확인하고, 해당 실행이 끝났음을 사람이 확인한 뒤 같은 run ID로만 `release`한다.
- 이 lease는 같은 로컬 Git 저장소의 큐를 막는다. 다른 머신까지 동시 실행해야 한다면 별도의 atomic CAS lease 없이는 지원하지 않는다.

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

이 권한에는 관리 명세·상태·담당자·댓글 갱신, 격리 worktree 구현, 검증, 해당 작업의 commit, 일반 push, draft PR 생성·갱신, 리뷰 수정 commit, draft 해제, 사람 검토 요청이 포함된다. 실제 GitHub merge, `main` 변경, 배포, 운영 URL 검사, Notion `완료` 처리는 포함되지 않는다.

force push, amend, rebase, branch·worktree·PR 삭제, 관련 없는 사용자 변경 포함, self-approval, 제품 결정 추측은 하지 않는다.

Notion에는 프로젝트 `.codex/config.toml`의 이름이 정확히 `notion`인 MCP만 사용한다. 노출된 도구 이름이 있다면 `mcp__notion__...`만 허용한다. 다른 Notion 플러그인, 브라우저 자동화, 직접 API 호출로 우회하지 않는다.

## 실행 상태

한 번에 `active_task` 하나만 유지한다.

- `completed_this_run`: `$notion-request-review`까지 끝난 작업 ID
- `topic_review_this_run`: 주제 검토로 넘긴 작업 ID
- `deferred_this_run`: 이번 실행에서 기술 실패로 일시중단한 작업 ID
- `active_task`: 작업 ID, 페이지 ID, 현재 단계, spec revision, branch, worktree, PR, latest head SHA

모든 하위 호출에 정확한 `작업 ID`를 명시하고 제목이나 URL로 대신하지 않는다.

## 후보 선택과 재개 lane

매 반복에서 신규 작업보다 먼저 StoryG Blog relation과 `상태=명세`인 작업을 조회한다. 이번 실행의 완료·인계·보류 집합을 제외하고 작업 ID 숫자가 작은 항목부터 하나를 재개한다.

재개할 `명세` 작업이 없을 때만 `$notion-select-task`를 자동 큐 모드로 호출한다. 신규 후보는 `일시중단`, `시작 전`, `백로그`뿐이다.

- `진행 중`은 새 큐에서 완전히 제외하고 사람이 재개 여부를 판단한다.
- `주제 검토 요청`, `검토 중`, `완료`, `취소`, `보관`, `모니터링`도 제외한다.
- 종료 전에 제외된 `진행 중` 작업 ID와 확인 가능한 branch·PR을 별도 보고한다.

## 산출물 기반 단계 판정

선택한 작업의 상태만 보지 말고 다음 산출물을 exact task linkage로 검증한다. 가장 높은 일관된 산출물이 현재 단계다.

1. 실제 검토 요청 marker·mention과 최신 PR head가 일치함: 검토 요청 완료
2. ``notion-create-project-pr/v1`` 연결, open PR, branch, head SHA가 일치함: PR 리뷰 단계
3. 검증된 작업 branch·worktree가 같은 ID와 연결됨: 구현 또는 PR 생성 단계
4. 자동 확정 명세, 승인 내용 hash, `명세리뷰=리뷰완료`가 일치하거나 legacy v1 확정 기록과 `리뷰완료`가 일치함: 구현 대기
5. 자동 확정 명세가 있으나 `명세리뷰` 속성이 미완료임: 명세 리뷰 부분 성공 복구
6. 검토 초안과 `명세리뷰=리뷰전`이 일치함: 명세 리뷰
7. 검토 초안이 있으나 `명세리뷰`가 비어 있음: 명세 초안 부분 성공 복구
8. 관리 명세가 없음: 분석 시작

branch 이름만으로 단계를 올리지 않는다. marker, task ID, branch, PR, head가 함께 맞아야 한다.

- legacy v1 marker와 댓글은 삭제하지 않고 기존 형식대로 계속 인식한다.
- 상태보다 높은 산출물이 `일시중단`, `시작 전`, `백로그`, `명세` 작업에서 확인되면 산출물을 다시 만들지 않는다.
- 검증된 worktree 또는 open PR이 있으면 durable 하위 증거를 먼저 확인한 뒤 상태를 `진행 중`으로 투영하고 해당 단계부터 같은 실행에서 재개한다.
- 명세 산출물까지만 있으면 상태를 `명세`로 유지하거나 `$notion-analyze-task`를 통해 전환한다.
- `진행 중`, `검토 중`, 종료 상태를 더 이른 상태로 되돌리지 않는다.
- 검토 초안인데 `명세리뷰=리뷰완료`인 조합은 자동 보정하지 않고 불일치로 처리한다.
- 산출물과 linkage가 충돌하면 추측해 상태를 바꾸지 않고 `일시중단` 분기로 보낸다.

## 작업별 실행

산출물 판정 뒤 필요한 첫 단계부터 실행한다.

1. 구현 이후 산출물이 없을 때만 다음을 적용한다.
   - 관리 명세가 없거나 상태가 아직 `명세`가 아니면 `$notion-analyze-task`로 `명세` 전환·분석을 수행한다.
   - 검토 초안이 있고 현재 queue 실행에 같은 ID의 분석 결과가 없으면 `$notion-analyze-task`를 `명세` no-op 재개로 실행한다.
   - durable 자동 확정 명세가 있으면 현재 실행의 분석 결과가 없어도 재분석하지 않는다.
2. 확정 명세가 없으면 `$notion-specify-task`로 초안을 저장한다.
3. 초안이거나 자동 확정 명세의 `명세리뷰`가 미완료면 `$notion-review-spec`을 실행한다. 승인 hash가 일치하는 부분 성공은 본문을 다시 쓰지 않고 속성만 복구한다.
4. 확정 명세면 `$notion-implement-task`로 worktree를 준비하고 `명세 → 진행 중`으로 전환해 구현한다.
5. 검증된 구현이면 `$notion-create-pr`로 commit·push·draft PR을 연결한다.
6. `$notion-review-pr`로 latest head가 승인 가능할 때까지 독립 reviewer와 단일 fixer를 반복한다.
7. `$notion-request-review`로 garam에게 배정하고 `검토 중` 및 실제 mention 댓글을 기록한다.

완료 증거가 온전한 단계는 건너뛴다. 높은 단계 산출물은 모든 낮은 단계의 durable 필수 증거가 함께 일치할 때만 유효하다. 여기서 mutable `상태`는 durable 증거 검사에서 제외한다.

예를 들어 PR이 있으면 확정 명세, `명세리뷰=리뷰완료`, task ID, branch, head, PR linkage를 먼저 검증한다. 그 뒤 `일시중단` 같은 상태를 `진행 중`으로 투영하고 child 사전 조건을 다시 확인한다.

후기 산출물은 일치하지만 구현 시작 댓글이나 검증 기록만 빠졌으면 기존 PR·commit을 폐기하지 않는다. 상태 투영 뒤 `$notion-implement-task`의 후기 산출물 증거 복구 경로로 댓글과 검증만 보충한 후 PR 단계로 돌아간다.

부분 성공이면 외부 상태를 재조회하고 마지막 성공 지점 다음부터 재개한다. 기존 worktree, commit, push, PR, 댓글을 중복 생성하지 않는다.

`진행 중` 전환 뒤에는 현재 실행의 `active_task`를 계속 처리한다. 프로세스가 끝난 뒤 새 큐가 시작되면 `진행 중`을 자동 재개하지 않는 기존 정책을 지킨다.

## 주제 검토 분기

분석 또는 명세 리뷰에서 다음이 확인되면 구현하지 않고 `$notion-request-topic-review`에 정확한 작업 ID, 구체적 사유, 사람이 결정할 내용을 전달한다.

- 작업이 무의미하거나 StoryG Blog 목표와 무관함
- 서로 모순된 요구 때문에 결과를 정할 수 없음
- 제품·주제 선택 없이는 검증 가능한 명세를 만들 수 없음
- 선행 결정이 없어 현재 형태로 진행할 가치가 없음

`명세 → 주제 검토 요청` 인계를 재조회로 검증한 뒤 다음 후보로 이동한다.

## 기술 실패와 사건별 중단 기록

Notion·GitHub·CI·network·tool 오류, flaky test, rate limit은 주제 검토 사유가 아니다.

- 같은 작업의 같은 단계는 최초 시도 뒤 최대 2회 재시도한다.
- 재시도 전 이미 성공한 상태·commit·push·PR·댓글을 재조회한다.
- 세 번째 실패 뒤 상태를 안전하게 쓸 수 있으면 `일시중단`으로 바꾸고 사건별 댓글을 남긴다.

```text
[codex-task-paused/v2]

실행 키: TODO-123:<단계>:<spec-revision-or-head>:<failure-fingerprint>
실패 단계: <단계>
증거: <오류·CI·도구 결과>
재개 지점: <다음에 시작할 단계>
```

- 중복 방지 키는 작업 ID, 단계, spec revision 또는 head SHA, 안정적인 failure fingerprint다.
- 같은 실행 키의 댓글만 중복으로 막고, 이후 다른 단계·revision·실패 사건은 새 댓글을 허용한다.
- 기존 ``[codex-task-paused/v1]`` 댓글은 보존하고 legacy 이력으로 인식한다.
- 상태나 댓글 쓰기에 실패하면 현재 산출물을 보존하고 수동 재개 대상으로 보고한다.

해당 ID를 `deferred_this_run`에 넣고 다음 후보로 이동한다. 프로젝트 Notion MCP 또는 GitHub가 모든 후보에 공통으로 필요한데 서비스 전체 장애나 권한 문제로 사용할 수 없을 때만 전체 큐를 중단한다.

## 종료

작업이 `$notion-request-review`까지 끝나면 `completed_this_run`에 넣고 다시 재개 lane부터 조회한다.

- 정상 종료: 제외 집합 적용 뒤 `명세` 재개 작업과 `일시중단`, `시작 전`, `백로그` 신규 후보가 모두 없음
- 전역 중단: 공통 의존성 장애로 어떤 후보도 안전하게 처리할 수 없음

최종 보고에는 작업 ID별 `검토 요청 완료`, `주제 검토 요청`, `일시중단`, `수동 확인할 진행 중`을 구분하고 PR URL, latest head, 실패 재개 지점을 포함한다. merge와 배포를 수행하지 않았음을 명시한다.
