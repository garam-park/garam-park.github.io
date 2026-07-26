---
name: notion-request-topic-review
description: Hand off exactly one StoryG Blog Notion task identified by an explicit exact task ID when it is meaningless, not actionable, or blocked on a product or topic decision rather than a transient technical failure. Assign garam without removing other assignees, move the task to 주제 검토 요청, and add one idempotent real-mention comment containing the concrete reason and needed decision. Use from notion-run-queue or directly when analysis or specification review proves that human topic review is required. Do not use for temporary Notion, GitHub, CI, network, or tooling failures.
---

# Notion 주제 검토 요청

자동으로 진행할 수 없는 작업을 사람의 주제 판단 단계로 안전하게 인계한다.

## 작업 ID와 사유 계약

- 현재 요청에 `작업 ID: <정확한 값>`, 구체적인 `사유`, 사람이 정할 `확인 필요`가 있어야 한다.
- 이전 대화, 제목, URL, 페이지 UUID만으로 작업 ID를 추론하지 않는다.
- 데이터베이스 `ID` unique_id에 exact match하고 StoryG Blog relation을 확인한다.
- 다음 중 하나의 근거가 있어야 한다.
  - 작업 목표가 없거나 현재 프로젝트와 무관함
  - 요구가 서로 모순되어 구현 결과를 정할 수 없음
  - 제품·주제 선택 없이는 검증 가능한 명세를 만들 수 없음
  - 선행 결정이 없어 현재 형태로는 실행할 의미가 없음
- 일시적인 Notion·GitHub·CI·network·tool 오류에는 이 스킬을 사용하지 않는다.

## 권한과 경계

정확한 작업 ID와 근거를 포함한 호출은 다음 Notion 변경만 승인한다.

1. 기존 담당자를 보존하며 `garam`을 `담당자`에 포함
2. `상태`를 `주제 검토 요청`으로 변경
3. 실제 garam user mention, 사유, 확인 필요가 포함된 페이지 댓글을 한 번 작성

Notion 본문, 다른 속성·페이지, 파일, Git, GitHub, CI, merge, 배포는 변경하지 않는다.

Notion에는 이 저장소 `.codex/config.toml`의 이름이 정확히 `notion`인 MCP만 사용한다. 노출된 도구 이름이 있다면 `mcp__notion__...`만 허용한다. 다른 Notion 플러그인, `mcp__codex_apps__notion`, 브라우저 자동화, 직접 API 호출로 우회하지 않는다.

## 고정 대상

| 대상 | 값 |
| --- | --- |
| 프로젝트 페이지 ID | `3a48e829-7400-81a5-9f3c-cfd701dd3c6c` |
| 할 일 data source ID | `3a28e829-7400-80b2-80bf-000bb0ab59ac` |
| 작업 ID 속성 | `ID` (`unique_id`, prefix `TODO`) |
| 담당자 속성 | `담당자` (`people`) |
| 검토 상태 | `주제 검토 요청` |
| 검토자 | `garam` |
| 검토자 user ID | `a0ffaf82-2f8c-4df5-ad5f-9c38a03a453a` |

실행할 때 data source, 상태 옵션, 사용자 ID와 유형을 다시 읽는다. 하나라도 다르면 추측해 변경하지 않는다.

## 실행 순서

### 1. 대상과 근거 확인

작업 ID를 exact match하고 StoryG Blog relation, 전체 속성·본문, 현재 댓글을 읽는다. 상태가 `백로그`, `시작 전`, `일시중단`, `명세`이거나 같은 자동 실행에서 막 도달한 `진행 중`일 때만 계속한다.

사유와 확인 필요를 독립된 사람이 이해할 수 있는 문장으로 정리한다. 단순히 “진행 불가”, “정보 부족”, 도구 오류만 적지 않는다.

### 2. 중복과 동시 변경 확인

쓰기 직전에 페이지와 댓글을 다시 읽는다.

- ``[codex-topic-review/v1]`` marker 댓글이 이미 있으면 새 댓글을 만들지 않는다.
- marker가 둘 이상이면 추가 쓰기를 중단하고 중복을 보고한다.
- `완료`, `취소`, `보관`, `모니터링`, `검토 중`으로 바뀌었으면 자동으로 되돌리지 않는다.
- 분석 또는 명세 리뷰에서 호출할 때는 최신 상태가 `명세`인지 확인하고 `명세 → 주제 검토 요청`으로만 전환한다.

### 3. 속성 갱신

하나의 property update로 다음을 적용한다.

- 기존 `담당자` 목록에 garam user ID가 없으면 추가하고, 다른 담당자는 제거하지 않는다.
- `상태.status.name`을 `주제 검토 요청`으로 설정한다.

재조회해 garam이 포함되고 상태가 정확한지 확인한다. 실패하면 댓글을 만들지 않는다.

### 4. 실제 멘션 댓글

marker가 없을 때 rich text 댓글을 다음 구조로 작성한다. `@garam` 문자열이 아니라 user ID를 가리키는 실제 `user` mention을 사용한다.

```text
[codex-topic-review/v1]

@garam 주제 검토가 필요합니다.
사유: <구체적인 진행 불가 근거>
확인 필요: <사람이 결정할 내용>
```

작성 뒤 marker, mention user ID, 사유, 확인 필요를 다시 읽어 확인한다.

## 중복 실행과 재개

- 실행 키는 작업 ID, marker, garam user ID다.
- 속성 갱신 뒤 댓글이 실패하면 속성을 되돌리지 않고 댓글부터 재개한다.
- 이미 속성과 댓글이 일치하면 쓰기 없이 완료한다.
- 기존 marker 댓글의 사유가 현재 근거와 다르면 댓글을 중복 작성하지 않고 차이를 보고한다.

## 완료 조건

- 상태가 `주제 검토 요청`
- 담당자에 garam이 포함됨
- 실제 garam mention과 사유·확인 필요가 있는 marker 댓글이 정확히 하나 존재

완료 뒤 현재 자동 큐에서는 해당 작업을 제외하고 다음 후보로 이동한다.
