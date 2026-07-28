---
name: notion-review-spec
description: Drive the managed specification of exactly one StoryG Blog Notion task identified by an explicit exact task ID to automatic approval with a multi-agent review-and-fix loop. Independent read-only reviewers define and judge specification approval conditions from requirements, repository impact, verification, risk, and applicable post-quality perspectives, while a separate fixer updates only the managed Notion specification. Repeat until every reviewer-owned condition passes, then record automatic multi-agent confirmation and set 명세리뷰 to 리뷰완료. Use after notion-specify-task saves a review draft, or to resume an interrupted specification review. Do not implement product code.
---

# Notion 명세 멀티에이전트 리뷰

독립 리뷰 에이전트들이 명세 승인 조건을 만들고 판정하게 한다. 별도 수정 에이전트는 관리 명세만 고치며 스스로 승인하지 못한다. 최신 명세가 모든 조건을 만족할 때까지 반복한 뒤 자동 확정한다.

## 작업 ID 계약

- 현재 요청에 `작업 ID: <정확한 값>`이 반드시 있어야 한다.
- 이전 대화, 제목, URL, 페이지 UUID만으로 대상을 추론하지 않는다.
- 데이터베이스 `ID` unique_id에 exact match하고 StoryG Blog relation을 확인한다.
- 일반 검토에서는 입력 ID, 분석 결과, 관리 명세가 같은 작업을 가리켜야 한다.
- durable 자동 확정 metadata와 matching 승인 내용 hash를 이용한 property-only 복구에서는 현재 실행의 분석 결과를 요구하지 않는다.
- 누락, 0건, 중복, 연결 불일치면 Notion을 변경하지 않는다.

## 권한과 경계

정확한 작업 ID를 포함해 이 스킬을 실행해 달라는 요청은 다음을 승인한 것으로 본다.

- 여러 읽기 전용 명세 reviewer 생성
- 대상 본문의 ``notion-specify-project-task/v1`` 관리 구역만 반복 수정
- 검토 통과 뒤 관리 구역에 자동 확정 기록
- `명세리뷰`를 `리뷰완료`로 변경

다음은 하지 않는다.

- 사용자 작성 본문이나 다른 관리 구역 변경
- `명세리뷰` 외 Notion 속성 또는 다른 페이지 변경
- 제품 코드·문서·테스트 수정
- branch, worktree, commit, push, PR, CI, merge, 배포
- reviewer의 명세 수정
- 수정 에이전트의 조건 생성·면제·통과 판정

Notion에는 이 저장소 `.codex/config.toml`의 이름이 정확히 `notion`인 MCP만 사용한다. 노출된 도구 이름이 있다면 `mcp__notion__...`만 허용한다. 다른 Notion 플러그인, `mcp__codex_apps__notion`, 브라우저 자동화, 직접 API 호출로 우회하지 않는다.

## 고정 대상

| 대상 | 값 |
| --- | --- |
| 프로젝트 | `StoryG Blog` |
| 프로젝트 페이지 ID | `3a48e829-7400-81a5-9f3c-cfd701dd3c6c` |
| 할 일 data source ID | `3a28e829-7400-80b2-80bf-000bb0ab59ac` |
| 작업 ID 속성 | `ID` (`unique_id`, prefix `TODO`) |
| 명세 리뷰 속성 | `명세리뷰` |
| 검토 전 값 | `리뷰전` |
| 검토 완료 값 | `리뷰완료` |
| 포스트 Gate 페이지 ID | `3a88e829-7400-8131-a07a-ee01c056fc8e` |

실행할 때 스키마와 옵션을 다시 읽는다. 이름이나 ID가 달라졌으면 추측해 쓰지 않는다.

## 역할 분리

### 오케스트레이터

- TODO, 분석, 관리 명세, 저장소 snapshot을 한 작업 ID로 연결한다.
- 동일한 snapshot을 reviewer들에게 전달한다.
- reviewer 조건의 합집합을 보존한다.
- writer를 한 번에 하나만 실행한다.
- reviewer 판정 뒤에만 `리뷰완료`를 기록한다.
- 조건을 임의로 추가·삭제·통과시키지 않는다.

### 리뷰 에이전트

최소 세 관점을 서로의 결론을 보지 않게 병렬 실행한다. 슬롯이 부족하면 읽기 전용 reviewer를 여러 wave로 실행한다.

1. `requirements-reviewer`: 배경, 목표, 비범위, 요구사항, 열린 질문, 내부 일관성
2. `repository-reviewer`: 현재 코드·문서 구조와 예상 변경 대상, 구현 가능성, 호환성
3. `verification-reviewer`: 검증 가능한 완료 조건, 테스트 계획, 위험, 의존성, 실패 경로
4. `post-spec-reviewer`: 새 글 또는 실질적 개편 글의 독자·환경·출처·포스트 Gate 반영

각 reviewer는 다음 형식만 반환한다.

```text
reviewer: <역할>
spec_revision: <검토한 page last_edited_time과 관리 구역 hash>
verdict: APPROVE | CHANGES_REQUIRED | BLOCKED
conditions:
  - id: <역할-prefix와 안정적인 번호>
    status: PASS | FAIL | BLOCKED
    severity: P0 | P1 | P2 | P3
    requirement: <명세 확정 전에 참이어야 하는 검증 가능한 문장>
    evidence: <Notion 구역, 저장소 파일 또는 분석 근거>
    correction: <명세에 필요한 최소 수정>
    verification: <수정 후 재검증 방법>
notes: <확정 차단이 아닌 관찰>
```

취향, 구현 세부 선호, 명세 밖 확장은 조건으로 만들지 않는다. 확인되지 않은 제품 결정을 reviewer가 대신 만들지 않는다.

### 수정 에이전트

- FAIL 조건만 입력받아 관리 명세 구역의 최소 문장만 수정한다.
- 분석·저장소에서 확인되지 않은 사실을 만들지 않는다.
- 목표와 비범위를 바꾸는 제품 결정은 자동 선택하지 않는다.
- 수정 뒤 저장된 관리 구역과 기존 사용자 본문 보존을 재조회한다.
- 조건을 PASS로 판정하거나 `명세리뷰`를 변경하지 않는다.

## 실행 순서

### 1. 대상과 초안 확인

다음을 공통으로 확인한다.

1. 작업이 StoryG Blog에 연결되고 상태가 정확히 `명세`임
2. ``notion-specify-project-task/v1`` marker가 정확히 하나 있음
3. 관리 구역의 `명세 상태`가 `검토 초안` 또는 `확정`임
4. 목표, 비범위, 요구사항, 완료 조건, 예상 변경 대상, 검증 계획이 있음

`백로그`, `시작 전`, `일시중단`이면 먼저 `$notion-analyze-task`로 `명세` 전환과 분석을 수행한다. `진행 중` 이후 상태를 되돌리지 않는다.

기존 관리 구역과 `명세리뷰` 조합은 다음처럼 처리한다.

- `검토 초안`이면 `명세리뷰=리뷰전`일 때만 새 검토를 시작한다.
- 자동 확정 기록과 `리뷰완료`가 모두 있으면 현재 내용 hash가 저장된 승인 hash와 일치하는지 확인하고 완료로 보고한다. 승인 hash가 없는 기존 v1 확정 기록은 legacy 완료로 인정하되 다른 불일치가 없어야 한다.
- 자동 확정 기록은 있으나 `리뷰완료`가 아니고 저장된 승인 hash가 현재 내용과 일치하면, 본문을 다시 쓰지 않고 `리뷰완료` 속성만 복구한다.
- 자동 확정 기록은 있으나 승인 hash가 없으면 동일 최신 snapshot을 reviewer들이 다시 검토해 승인한 뒤 새 확정 metadata와 속성을 기록한다.
- `명세리뷰=리뷰완료`인데 관리 구역이 초안이거나 확정 증거가 없으면 자동으로 사실을 만들거나 속성을 내리지 않고 불일치를 보고한다.

### 2. snapshot 생성

일반 검토에서는 작업 ID, 전체 속성·본문, 분석 결과, 관리 명세, 관련 저장소 파일, 현재 base SHA를 읽는다. 포스트 작업이면 프로젝트 Notion MCP로 포스트 Gate를 최신 상태로 읽는다.

property-only 복구에서는 작업 ID, 전체 속성·본문, 관리 명세, 저장된 승인 내용 hash를 읽고 현재 내용 hash를 다시 계산한다. 둘이 일치하면 분석 결과와 reviewer 재실행 없이 `명세리뷰`만 복구할 수 있다.

snapshot은 page last_edited_time과 관리 구역 hash로 식별한다. 모든 reviewer가 같은 revision을 검토해야 한다.

내용 hash는 관리 구역에서 `명세 상태`, `확정 방식`, `명세 리뷰 라운드`, `명세 승인 내용 hash`, `명세 reviewer` 감사 metadata 줄을 제외한 나머지 내용을 정규화해 SHA-256으로 계산한다.

### 3. 승인 조건 생성

reviewer들을 독립 실행하고 모든 P0~P3 조건을 합집합으로 보존한다.

- 같은 원인과 검증법을 가진 조건만 연결하고 원래 ID와 소유 reviewer를 유지한다.
- 명세 또는 분석과 충돌하거나 사람의 제품 결정이 필요한 조건은 `BLOCKED`다.
- 최초 조건은 검증 계약이며 새 증거나 수정으로 생긴 위험이 있을 때만 추가한다.
- BLOCKED가 있으면 명세를 임의 확정하지 않고 사유를 반환한다.

### 4. 명세 수정

FAIL 조건을 단일 수정 에이전트에 전달한다. 수정 뒤 page revision을 다시 읽고, 예상하지 못한 동시 편집이 있으면 덮어쓰지 않는다.

새 revision으로 원래 reviewer 관점들을 새 에이전트에 맡겨 다시 검토한다. reviewer는 자기 조건만 닫을 수 있고, 이전 revision의 PASS를 자동 승계하지 않는다. `CHANGES_REQUIRED`이면 수정과 재검토를 반복한다.

### 5. 자동 확정

같은 최신 revision에 대해 모든 reviewer가 APPROVE하고 모든 조건이 PASS면 관리 구역의 metadata를 다음으로 교체한다.

```text
명세 상태: 확정
확정 방식: 자동 멀티에이전트 검토
명세 리뷰 라운드: <횟수>
명세 승인 내용 hash: <감사 metadata를 제외한 관리 구역 SHA-256>
명세 reviewer: requirements-reviewer, repository-reviewer, verification-reviewer[, post-spec-reviewer]
```

관리 구역을 재조회해 상태가 여전히 `명세`이고 저장된 hash가 현재 내용에서 다시 계산한 hash와 일치하는지 확인한 뒤에만 `명세리뷰`를 `리뷰완료`로 변경한다. 속성을 다시 읽어 실제 값을 검증한다.

## 중복 실행과 재개

- 실행 키는 작업 ID, page revision, review round다.
- 중단되면 현재 관리 구역과 `명세리뷰`를 다시 읽고 미완료 조건부터 재개한다.
- 같은 실행 안에서는 완료된 reviewer 결과를 재사용한다.
- 프로세스가 다시 시작됐고 durable 확정 hash가 없으면 동일 revision이라도 읽기 전용 reviewer를 다시 실행한다. reviewer 재실행은 안전한 검증이며 확정 증거를 추측하는 것보다 우선한다.
- 동시 편집, reviewer 실패, Notion 쓰기 실패가 있으면 완료된 결과를 보존한다.
- 반복해도 진전이 없거나 BLOCKED면 자동 확정하지 않는다.

## 완료 조건

일반 검토는 다음을 모두 재조회로 확인하면 끝낸다.

- 같은 최신 revision에 대한 모든 reviewer verdict가 APPROVE
- 모든 reviewer 소유 조건이 PASS
- 관리 구역에 자동 확정 metadata가 있음
- 새 형식이면 저장된 승인 내용 hash가 현재 관리 구역에서 다시 계산한 hash와 일치함
- `명세리뷰`가 `리뷰완료`임
- `상태`가 `명세`로 유지됨
- 사용자 본문과 다른 속성이 보존됨

property-only 복구는 다음을 모두 확인하면 끝낸다.

- durable 자동 확정 metadata가 있음
- 저장된 승인 내용 hash와 현재 내용 hash가 일치함
- `명세리뷰`가 `리뷰완료`로 복구됨
- `상태=명세`와 사용자 본문이 보존됨

```text
다음 호출: $notion-implement-task 작업 ID: <정확한 값>
```
