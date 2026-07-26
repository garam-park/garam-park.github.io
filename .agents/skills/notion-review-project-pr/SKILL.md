---
name: notion-review-project-pr
description: Review a StoryG Blog pull request against its approved Notion task specification, current head SHA, diff, tests, and CI without changing anything. For new or substantially revised blog posts, also evaluate the applicable pre-deployment requirements from the Notion document "블로그 검색 최적화 확인 사항"; skip that gate for non-post work. Use when the user asks whether a PR correctly fulfills its task, wants actionable review findings, or needs a merge-readiness assessment before fixes or approval.
---

# Notion 프로젝트 PR 리뷰

PR이 확정 명세를 올바르게 수행했는지 검토하고, 포스트 작업이면 검색 최적화 Gate까지 판정한 뒤 읽기 전용 보고서로 끝낸다.

## 작업 경계

- Notion TODO, 확정 명세, PR diff, head SHA, CI를 읽는다.
- 명세 요구사항별 구현 증거와 누락을 확인한다.
- 정확성, 회귀, 보안, 성능, 접근성, 유지보수성 문제를 찾는다.
- 포스트 작업에만 별도 검색 최적화 Gate를 적용한다.
- 파일, branch, commit, PR, review comment, CI, Notion을 변경하지 않는다.
- 수정 구현, push, 승인, merge, 배포를 하지 않는다.

Notion에는 이 저장소 `.codex/config.toml`의 서버 이름이 정확히 `notion`인 MCP 조회 도구만 사용한다. 도구 이름이 노출된다면 `mcp__notion__...`만 허용한다. 다른 Notion 플러그인, `mcp__codex_apps__notion`, 브라우저 자동화, 직접 API 호출로 우회하지 않는다.

GitHub에는 연결된 GitHub 조회 도구를 우선 사용하고, thread 상태나 check 로그에 필요할 때만 `gh`의 읽기 명령을 사용한다.

## 고정 대상

| 대상 | 값 |
| --- | --- |
| 프로젝트 | `StoryG Blog` |
| 프로젝트 페이지 ID | `3a48e829-7400-81a5-9f3c-cfd701dd3c6c` |
| 할 일 데이터베이스 ID | `3a28e829-7400-808f-b53b-c35b8fef93a8` |
| GitHub 저장소 | `garam-park/garam-park.github.io` |
| 포스트 Gate 문서 | `블로그 검색 최적화 확인 사항` |
| 포스트 Gate 페이지 ID | `3a88e829-7400-8131-a07a-ee01c056fc8e` |

## 실행 순서

### 1. 대상 연결 확인

TODO와 PR을 하나로 식별하고 다음 연결을 검증한다.

1. TODO가 StoryG Blog에 연결됨
2. TODO 본문에 확정 명세 marker ``notion-specify-project-task/v1``가 하나 있음
3. PR 또는 Notion 연결 기록의 TODO ID, branch, head SHA가 일치함
4. 리뷰 대상이 PR의 최신 head SHA임
5. base branch 대비 전체 diff와 최신 CI 결과를 읽을 수 있음

연결이 불명확하거나 PR head가 바뀌었으면 오래된 diff를 리뷰하지 말고 최신 상태를 다시 읽는다.

### 2. 명세 준수 검토

확정 명세의 목표, 비범위, 요구사항, 완료 조건, 검증 계획을 항목별로 추출한다. 각 항목을 다음 중 하나로 판정한다.

- `충족`: 코드·문서·테스트에서 직접 증거를 확인함
- `부분 충족`: 일부 경로나 조건만 구현됨
- `미충족`: 요구된 동작 또는 검증이 없음
- `확인 불가`: 외부 환경 또는 배포 후 검증이 필요함

추측이나 PR 설명만으로 `충족` 처리하지 않는다. 파일·line, 테스트, CI log 등 재현 가능한 증거를 연결한다. 명세 밖 변경은 필요성과 위험을 별도로 검토한다.

### 3. 구현 품질 검토

전체 diff를 읽고 실제로 수정해야 하는 문제만 찾는다.

- `P0`: 즉시 중단해야 하는 보안·데이터 손실·서비스 장애
- `P1`: merge 전에 반드시 고쳐야 하는 명세 위반·주요 회귀
- `P2`: 일반적인 결함·누락된 예외 처리·중요한 검증 부족
- `P3`: 낮은 위험의 유지보수성·명확성 개선

각 finding에는 짧은 제목, 영향, 재현 조건, 근거 파일과 가능한 한 좁은 line 범위, 권장 수정 방향을 포함한다. 근거 없는 스타일 선호나 명세 밖 확장은 finding으로 만들지 않는다.

CI가 실패했으면 실패한 check와 로그 원인을 명세 준수 문제와 구분한다. CI가 아직 끝나지 않았으면 최종 승인 가능으로 판정하지 않는다.

### 4. 포스트 작업 판정

다음 중 하나면 포스트 작업으로 본다.

- `_posts/**` 또는 `_draft/**`에 새 글을 추가함
- 기존 글의 기술 내용, 명령, 버전, 구성, 결론, 메타데이터를 실질적으로 개편함
- Notion 명세가 새 포스트 작성, 포스트 개편, 검색 최적화를 명시함

오탈자·띄어쓰기·링크 한 건 같은 경미한 교정이나 코드·템플릿·인프라 작업이면 포스트 Gate를 생략하고 이유를 보고한다.

### 5. 포스트 검색 최적화 Gate

포스트 작업일 때만 프로젝트 Notion MCP로 Gate 페이지를 최신 상태로 읽는다. 페이지를 읽을 수 없으면 기준을 추측하지 말고 `확인 불가`로 판정한다.

문서의 다음 범위를 원문 그대로 기준으로 사용한다.

- 2장 작성 전 브리프
- 3장 front matter와 메타데이터
- 4장 본문 품질
- 5장 AI 검색 친화성
- 6장 Google 전용 배포 Gate
- 7장 Naver 전용 배포 Gate

대표 이미지가 없으면 이미지 전용 항목은 조건부 제외한다. 새 URL의 운영 HTTP 200, Search Console, 서치어드바이저처럼 배포 전 확인할 수 없는 항목은 실패가 아니라 `배포 후 확인 대기`로 분리한다. 8장 배포 후 검증은 merge 차단 finding으로 만들지 않는다. 9장 플랫폼 정비 항목은 현재 PR 명세에 포함되지 않으면 별도 후속 과제로만 보고한다.

소스와 local build 결과에서 확인 가능한 공통·Google·Naver 항목 중 하나라도 실패하면 `미통과`다. 모두 충족하고 배포 후 항목만 남으면 `배포 후 확인 대기`, 조건부 이미지 항목만 제외됐으면 `조건부 통과`다.

### 6. 결과 보고

다음 순서로 보고한다.

1. actionable findings를 심각도순으로 제시
2. 명세 완료 조건별 `충족/부분 충족/미충족/확인 불가` 표
3. CI와 테스트 상태
4. 포스트 여부와 판정 근거
5. 포스트라면 공통·Google·Naver Gate 및 전체 판정
6. merge 준비도: `수정 필요`, `CI 대기`, `배포 후 확인 대기`, `승인 가능`

포스트 Gate 기록에는 원본 문서 10장의 형식을 사용해 URL, 핵심 질문·독자, 적용 환경·제외 범위, 세 Gate 판정, 조건부 항목, 보완 항목을 포함한다.

finding이 없으면 “차단 finding 없음”이라고 명시하되 잔여 위험과 배포 후 확인 항목은 따로 적는다.

## 완료 조건

최신 PR head가 확정 명세를 얼마나 충족하는지 증거와 함께 판정하고, 포스트 작업에는 검색 최적화 Gate 결과까지 제공하면 끝낸다. 어떤 시스템도 변경하지 않는다.
