#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEFAULT_PACKAGE_SPEC="@notionhq/notion-mcp-server@2.4.1"

if [[ -n "${MCP_NOTION_ENV_FILE:-}" ]]; then
    ENV_FILE="$MCP_NOTION_ENV_FILE"
elif [[ -f "$SCRIPT_DIR/.env.local" ]]; then
    ENV_FILE="$SCRIPT_DIR/.env.local"
else
    ENV_FILE="$SCRIPT_DIR/.env"
fi

if [[ -f "$ENV_FILE" ]]; then
    set -a
    # shellcheck disable=SC1090
    source "$ENV_FILE"
    set +a
fi

if [[ -z "${MCP_NOTION_TOKEN:-}" ]]; then
    echo "Missing MCP_NOTION_TOKEN in $ENV_FILE" >&2
    exit 65
fi

export NOTION_TOKEN="$MCP_NOTION_TOKEN"
export OPENAPI_MCP_HEADERS="$(
    node -e 'process.stdout.write(JSON.stringify({
        Authorization: `Bearer ${process.env.NOTION_TOKEN}`,
        "Notion-Version": "2026-03-11",
    }))'
)"

exec npx -y "$DEFAULT_PACKAGE_SPEC"
