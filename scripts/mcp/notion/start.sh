#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ENV_FILE="${MCP_NOTION_ENV_FILE:-"$SCRIPT_DIR/.env"}"
MODE="${1:-read-write}"
DEFAULT_PACKAGE_SPEC="@notionhq/notion-mcp-server@2.4.1"

if [[ -f "$ENV_FILE" ]]; then
    set -a
    # shellcheck disable=SC1090
    source "$ENV_FILE"
    set +a
fi

case "$MODE" in
    default|read-write|write|writes|local)
        ;;
    *)
        echo "Usage: $0 [read-write]" >&2
        exit 64
        ;;
esac

if [[ -z "${MCP_NOTION_TOKEN:-}" ]]; then
    echo "Missing MCP_NOTION_TOKEN in $ENV_FILE" >&2
    exit 65
fi

export NOTION_TOKEN="$MCP_NOTION_TOKEN"

exec npx -y "$DEFAULT_PACKAGE_SPEC"
