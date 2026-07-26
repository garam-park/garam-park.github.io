---
name: notion-review-pr
description: >-
  Drive the pull request for exactly one StoryG Blog Notion task identified by an explicit exact task ID to approval-ready quality with a multi-agent review-and-fix loop. Independent reviewers define and judge merge approval conditions while a separate fixer implements verified changes. Repeat until every condition passes, CI is green, and no actionable review thread remains. Use when the user supplies `작업 ID: ID값` plus the existing PR and asks to review, address, fix, or prepare it for approval. Stop before merge or deployment.
---

# Notion 프로젝트 PR 멀티에이전트 리뷰

독립 리뷰 에이전트들이 merge 승인 조건을 만들고 판정하게 한다. 별도 수정 에이전트는 그 조건을 충족하도록 수정하되 스스로 승인하지 못하게 한다. 최신 head가 모든 조건을 만족할 때까지 반복하고 merge 전에 멈춘다.

## 작업 ID 계약

- 현재 요청에 `작업 ID: <정확한 값>`과 기존 PR 번호 또는 URL이 반드시 있어야 한다.
- PR, branch, 이전 대화만으로 작업 ID를 추론하지 않는다.
- 입력 ID를 데이터베이스에 exact match하고 TODO, 확정 명세, PR 연결 기록, branch가 모두 같은 ID를 가리키는지 확인한다.
- ID나 PR이 누락되거나 연결이 다르면 reviewer·수정 에이전트를 만들거나 외부 상태를 변경하지 않는다.

## 권한과 경계

정확한 작업 ID와 PR을 포함해 이 스킬을 실행해 달라는 요청은 다음을 승인한 것으로 본다.

- 리뷰 에이전트 생성과 읽기 전용 분석
- 기존 작업 branch와 worktree에서 확정 명세 범위의 수정
- 검증, 새 commit, 일반 push
- 기존 PR 갱신, 해결된 review thread 답변·resolve, draft 해제
- Notion의 기존 구현 연결 관리 구역에 최신 head·CI·review 상태 기록

다음은 허용하지 않는다.

- force push, amend, rebase, branch 삭제 또는 새 PR 생성
- 확정 명세의 실질적 확대나 변경
- 관련 없는 사용자 변경 포함
- 리뷰 에이전트의 파일 수정, commit, push, PR·Notion 변경
- 수정 에이전트의 승인 조건 생성·면제·통과 판정
- self-approval, merge, 배포, Notion 완료 처리

제품 결정, 명세 변경, 위험한 외부 변경이 필요할 때만 사용자에게 묻는다. 수정 가능한 finding이나 CI 실패가 남았다는 이유로 멈추지 않는다.

Notion에는 이 저장소 `.codex/config.toml`의 이름이 정확히 `notion`인 MCP만 사용한다. 노출된 도구 이름이 있다면 `mcp__notion__...`만 허용한다. 다른 Notion 플러그인, `mcp__codex_apps__notion`, 브라우저 자동화, 직접 API 호출로 우회하지 않는다.

GitHub에는 연결된 GitHub 도구를 우선 사용한다. review thread 상태와 Actions log처럼 필요한 기능이 없을 때만 `gh`를 사용한다. 인증 정보나 secret을 읽거나 출력하지 않는다.

멀티에이전트 실행 기능을 사용할 수 없으면 단일 에이전트 리뷰로 대체하지 말고 차단 사유를 보고한다.

## 고정 대상

| 대상 | 값 |
| --- | --- |
| 프로젝트 | `StoryG Blog` |
| 프로젝트 페이지 ID | `3a48e829-7400-81a5-9f3c-cfd701dd3c6c` |
| 할 일 데이터베이스 ID | `3a28e829-7400-808f-b53b-c35b8fef93a8` |
| GitHub 저장소 | `garam-park/garam-park.github.io` |
| 포스트 Gate 문서 | `블로그 검색 최적화 확인 사항` |
| 포스트 Gate 페이지 ID | `3a88e829-7400-8131-a07a-ee01c056fc8e` |

## 역할 분리

### 오케스트레이터

주 에이전트만 전체 흐름을 조정한다.

- TODO, PR, branch, worktree, 명세, head SHA를 연결한다.
- 동일한 snapshot과 raw artifact 위치를 리뷰 에이전트들에게 전달한다.
- reviewer 결과의 합집합으로 승인 조건부를 관리한다.
- 동시에 writer가 하나만 실행되도록 보장한다.
- reviewer 판정과 외부 CI 상태를 확인한 뒤 PR·Notion 연결 기록을 갱신한다.
- 승인 조건을 임의로 추가·삭제·통과시키지 않는다.

### 리뷰 에이전트

리뷰 에이전트는 서로의 결론을 보지 않고 같은 head를 독립 검토한다. 최소 세 관점을 병렬 실행하고, 포스트 작업이면 포스트 관점을 추가한다. 동시 실행 슬롯이 부족하면 읽기 전용 reviewer를 여러 wave로 실행한다.

1. `spec-reviewer`: 확정 명세, 비범위, 완료 조건, 사용자 기대
2. `code-reviewer`: 동작 정확성, 회귀, 경계 조건, 유지보수성
3. `verification-reviewer`: 테스트 적절성, CI, build·runtime·배포 위험, 보안·신뢰성
4. `post-reviewer`: 새 글 또는 실질적 개편 글의 내용 품질과 포스트 Gate

작업 특성상 중요한 별도 영역이 있으면 읽기 전용 전문 reviewer를 더할 수 있다. reviewer 수를 늘리는 것 자체를 목표로 삼지 않는다.

각 reviewer는 다음만 반환한다.

```text
reviewer: <역할>
head: <검토한 SHA>
verdict: APPROVE | CHANGES_REQUIRED | BLOCKED
conditions:
  - id: <역할-prefix와 안정적인 번호>
    status: PASS | FAIL | BLOCKED
    severity: P0 | P1 | P2 | P3
    requirement: <merge 전에 참이어야 하는 검증 가능한 문장>
    evidence: <파일·line, test, log 또는 명세 근거>
    verification: <통과를 재검증하는 방법>
notes: <merge 차단이 아닌 관찰>
```

근거 없는 스타일 선호나 명세 밖 확장은 조건으로 만들지 않는다. reviewer는 조건을 직접 수정하거나 해결하지 않는다.

### 수정 에이전트

수정 에이전트는 한 번에 하나만 실행한다.

- 오케스트레이터가 전달한 FAIL 조건과 CI·review thread만 대상으로 삼는다.
- 원인을 확인하고 최소 범위로 수정한다.
- 관련 테스트·lint·build와 `git diff --check`를 실행한다.
- 명시적인 파일만 stage하고 목적이 드러나는 새 commit을 만든 뒤 일반 push한다.
- 조건별 변경 파일, 검증 결과, 새 head SHA를 반환한다.

수정 에이전트는 조건을 바꾸거나 PASS로 판정하지 않는다. 기존 commit을 고쳐 쓰거나 history를 재작성하지 않으며 AI 관련 commit trailer, footer, 서명을 추가하지 않는다.

## 실행 순서

### 1. 대상과 snapshot 확인

입력한 작업 ID와 PR을 기준으로 다음을 읽고 하나의 검토 대상을 확정한다.

1. TODO가 StoryG Blog에 연결되고 상태가 `진행 중` 또는 `검토 중`임
2. TODO 본문에 확정 명세 marker ``notion-specify-project-task/v1``가 하나 있음
3. PR 또는 Notion 연결 기록의 TODO ID와 branch가 일치함
4. local worktree가 PR head branch에 연결됨
5. base branch 대비 전체 diff, 최신 CI, unresolved review thread를 읽을 수 있음

snapshot은 TODO ID, PR 번호, base SHA, head SHA, 명세 marker, CI run으로 구성한다. 모든 reviewer에게 같은 snapshot을 전달한다. PR head가 local보다 앞서면 안전하게 동기화하고, 예상하지 못한 divergence를 force로 해결하지 않는다.

### 2. 포스트 작업 판정

다음 중 하나면 포스트 작업으로 본다.

- `_posts/**` 또는 `_draft/**`에 새 글을 추가함
- 기존 글의 기술 내용, 명령, 버전, 구성, 결론, 메타데이터를 실질적으로 개편함
- 명세가 새 포스트 작성, 포스트 개편, 검색 최적화를 명시함

오탈자·띄어쓰기·링크 한 건 같은 경미한 교정이나 코드·템플릿·인프라 작업이면 포스트 Gate를 생략하고 근거를 기록한다.

포스트 작업일 때 오케스트레이터가 프로젝트 Notion MCP로 Gate 페이지를 최신 상태로 읽어 snapshot에 포함한다. `post-reviewer`는 2~7장을 검토한다. 대표 이미지가 없으면 이미지 전용 항목을 조건부 제외하고, 운영 HTTP 200·Search Console·서치어드바이저처럼 배포 뒤에만 확인 가능한 항목은 `배포 후 확인 대기`로 둔다. 8장은 merge 차단 조건으로 만들지 않고 9장은 명세 밖이면 후속 과제로만 기록한다.

### 3. 최초 승인 조건 생성

동일 snapshot으로 reviewer들을 병렬 실행한다. reviewer끼리 결과를 공유하지 않는다.

오케스트레이터는 결과를 원문 그대로 보존하고 다음 규칙으로 승인 조건부를 만든다.

- 모든 reviewer의 P0~P3 조건을 합집합으로 포함한다.
- 완전히 같은 원인과 검증법을 가진 조건만 연결하되 원래 ID와 소유 reviewer를 유지한다.
- 충돌하는 조건은 임의 선택하지 않고 reviewer 근거를 비교한다.
- 명세와 충돌하거나 제품 선택이 필요한 조건은 `BLOCKED`로 사용자에게 요청한다.
- 조건부는 `review round`, `head SHA`, `owner reviewer`, `status`, `evidence`를 기록한다.

최초 조건은 검증 계약이다. 이후 변경으로 새 위험이 생기거나 이전 snapshot에 없던 중대한 증거가 발견된 경우에만 reviewer가 새 조건을 추가할 수 있다. 취향 변경으로 조건을 계속 늘리지 않는다.

모든 reviewer가 `APPROVE`이고 조건이 전부 PASS면 6단계로 이동한다.

### 4. 수정

FAIL 조건, CI 실패, unresolved actionable review thread를 하나의 수정 묶음으로 만들어 단일 수정 에이전트에 전달한다.

수정 에이전트가 완료하면 오케스트레이터가 다음을 확인한다.

1. 지정 worktree와 branch만 변경했음
2. 관련 없는 변경이 없음
3. 보고한 테스트가 실제 성공했음
4. 새 commit과 remote head가 일치함

외부 장애나 명백한 일시 CI 오류는 코드 변경 없이 제한적으로 재실행할 수 있다. 같은 실패를 근거 없이 반복 수정하지 말고 원인을 다시 진단한다.

### 5. 재검토

push와 최신 CI 뒤 새 snapshot을 만든다. 원래 reviewer 관점들을 새 에이전트로 다시 실행하여 stale context와 자기 확증을 줄인다.

- 각 reviewer에게 기존 조건부와 최신 raw artifact를 전달한다.
- reviewer는 자기 관점의 모든 조건을 재검증하고 PASS·FAIL·BLOCKED를 판정한다.
- 다른 reviewer 소유 조건을 닫지 않는다.
- 수정으로 생긴 회귀나 새 증거가 있으면 새 조건을 추가할 수 있다.
- `APPROVE`는 자기 소유 조건이 모두 PASS이고 새 finding이 없을 때만 허용한다.

어떤 reviewer든 `CHANGES_REQUIRED`이면 4단계로 돌아간다. `BLOCKED`이면 오케스트레이터가 사용자 결정이나 외부 상태를 기다린다. 이전 head에 대한 PASS는 새 push 뒤 자동 승계하지 않는다.

### 6. 외부 review와 CI 정리

최신 head의 필수 CI가 모두 성공할 때까지 log를 진단하고 4~5단계를 반복한다.

review thread는 요청을 실제로 충족하고 reviewer 재검증이 끝난 뒤에만 commit SHA와 검증 결과를 답변하고 resolve한다. 해결하지 않은 요청을 dismiss하거나 임의로 resolve하지 않는다. 새 comment, 새 commit, base 변경이 생기면 새 snapshot으로 3~5단계를 반복한다.

### 7. Notion과 PR 상태 갱신

기존 ``notion-create-project-pr/v1`` 관리 구역이 정확히 하나 있을 때만 head commit, CI, review round와 상태를 최신 외부 상태에 맞춘다.

- `review: 수정 중`
- `review: 외부 승인 대기`
- `review: 승인 가능`

관리 구역이 없거나 중복됐으면 다른 본문을 만들거나 덮어쓰지 말고 연결 문제를 보고한다. 확정 명세와 다른 사용자 영역, Notion 속성은 변경하지 않는다.

모든 조건을 만족하고 PR이 draft면 ready for review로 전환한다. 실제 GitHub self-approval은 하지 않는다.

## 승인 가능 판정

오케스트레이터는 다음 증거가 모두 있을 때만 `승인 가능`으로 기록한다.

- 같은 최신 head를 검토한 모든 reviewer의 verdict가 `APPROVE`
- reviewer 소유 merge 승인 조건이 모두 `PASS`
- 모든 명세 완료 조건이 충족되거나 배포 후 항목만 확인 대기
- actionable P0~P3 finding과 unresolved actionable review thread가 없음
- 최신 head의 필수 CI가 모두 성공
- 포스트 작업이면 pre-deployment Gate 통과 또는 조건부 통과
- PR head·base·Notion 연결 기록이 최신 상태와 일치

저장소 정책상 사람 reviewer 승인이 필요하면 최종 외부 상태는 `외부 승인 대기`지만 구현 품질은 `승인 가능`으로 보고한다. reviewer 에이전트의 판정은 실제 GitHub approval이나 merge 권한을 대신하지 않는다.

## 중단과 재개

- 실행 키는 정확한 작업 ID, PR 번호, latest head SHA, review round다.
- 조건부와 reviewer 판정은 head SHA별로 구분한다.
- push 뒤 중단됐으면 기존 PR과 branch에서 재개하고 중복 commit·push를 만들지 않는다.
- reviewer 또는 수정 에이전트가 실패하면 완료된 결과를 보존하고 해당 역할만 다시 실행한다.
- 외부 장애, 권한 부족, 명세 변경 필요, 사용자 결정이 필요한 충돌에서만 멈춘다.
- 부분 성공을 되돌리거나 worktree·branch·PR을 삭제하지 않는다.

## 완료 조건

최신 head에 대해 모든 독립 reviewer가 자기 승인 조건을 PASS로 판정하고, 필수 CI와 외부 review thread가 정리되어 실제 사람이 승인할 수 있는 상태가 되면 끝낸다. merge와 배포는 별도 단계에 맡긴다.

```text
다음 호출: $notion-request-review 작업 ID: <정확한 값> PR: <PR URL>
```
