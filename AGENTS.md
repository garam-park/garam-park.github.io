## Notion 작업

- Notion 워크스페이스의 검색, 조회, 생성, 수정 작업은 반드시 이 프로젝트의 `notion` MCP 서버를 사용한다.
- 해당 서버는 `.codex/config.toml`에 등록되어 있으며 `scripts/mcp/notion/start.sh`로 실행된다.
- 다른 Notion 플러그인, 브라우저 자동화 또는 직접 API 호출로 대체하지 않는다.
- MCP 서버를 사용할 수 없으면 임의로 우회하지 말고 문제를 사용자에게 알린다.
- `scripts/mcp/notion/.env`의 인증 정보를 읽거나 출력하지 않는다.

## Git worktree

- 별도 worktree가 필요한 작업은 기본적으로 프로젝트 루트의 `.worktrees/<작업명>`에 생성한다.
- 생성하기 전에 `git worktree list`와 대상 브랜치의 존재 여부를 확인하여 경로 및 브랜치 충돌을 피한다.
- 사용자가 다른 위치를 지정하지 않았다면 프로젝트 외부나 형제 디렉터리에 worktree를 만들지 않는다.
- 기존 worktree나 연결된 브랜치는 사용자의 명시적인 요청 없이 삭제하지 않는다.
