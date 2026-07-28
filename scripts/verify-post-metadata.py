#!/usr/bin/env python3
"""Fail-closed source/front-matter to generated-HTML metadata verifier."""

from __future__ import annotations

import argparse
import ast
import json
import re
import sys
from datetime import datetime
from html.parser import HTMLParser
from pathlib import Path
from typing import Any


def parse_scalar(value: str) -> Any:
    value = value.strip()
    if not value:
        return ""
    if value.startswith("[") and value.endswith("]"):
        return [item.strip().strip("\"'") for item in value[1:-1].split(",")]
    if value.lower() in {"true", "false"}:
        return value.lower() == "true"
    if value[0:1] in {"\"", "'"}:
        return ast.literal_eval(value)
    return value


def parse_front_matter(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"\A---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
        raise ValueError(f"{path}: missing front matter")

    result: dict[str, Any] = {}
    for line in match.group(1).splitlines():
        if not line or line.startswith((" ", "\t", "#")):
            continue
        key, separator, value = line.partition(":")
        if not separator:
            raise ValueError(f"{path}: unsupported front matter line: {line}")
        result[key.strip()] = parse_scalar(value)
    return result


class MetadataParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.meta: dict[str, str] = {}
        self.canonical = ""
        self.title_parts: list[str] = []
        self.h1_parts: list[str] = []
        self.h1_values: list[str] = []
        self.json_ld: list[dict[str, Any]] = []
        self.has_mermaid_source = False
        self._in_title = False
        self._in_h1 = False
        self._in_json_ld = False
        self._script_parts: list[str] = []

    def handle_starttag(
        self, tag: str, attrs_list: list[tuple[str, str | None]]
    ) -> None:
        attrs = {key: value or "" for key, value in attrs_list}
        if tag == "meta":
            key = attrs.get("name") or attrs.get("property")
            if key:
                self.meta[key] = attrs.get("content", "")
        elif tag == "link" and "canonical" in attrs.get("rel", "").split():
            self.canonical = attrs.get("href", "")
        elif tag == "title":
            self._in_title = True
        elif tag == "h1":
            self._in_h1 = True
            self.h1_parts = []
        elif tag == "code" and "language-mermaid" in attrs.get("class", "").split():
            self.has_mermaid_source = True
        elif tag == "script" and attrs.get("type") == "application/ld+json":
            self._in_json_ld = True
            self._script_parts = []

    def handle_data(self, data: str) -> None:
        if self._in_title:
            self.title_parts.append(data)
        if self._in_h1:
            self.h1_parts.append(data)
        if self._in_json_ld:
            self._script_parts.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self._in_title = False
        elif tag == "h1" and self._in_h1:
            self.h1_values.append("".join(self.h1_parts).strip())
            self._in_h1 = False
        elif tag == "script" and self._in_json_ld:
            payload = "".join(self._script_parts).strip()
            self.json_ld.append(json.loads(payload))
            self._in_json_ld = False

    @property
    def title(self) -> str:
        return " ".join("".join(self.title_parts).split())


def find_json_ld(parser: MetadataParser, schema_type: str) -> dict[str, Any]:
    for item in parser.json_ld:
        if item.get("@type") == schema_type:
            return item
    raise ValueError(f"generated HTML: missing {schema_type} JSON-LD")


def expected_modified(front_matter: dict[str, Any]) -> datetime:
    raw = str(front_matter["last_modified_at"])
    return datetime.strptime(raw, "%Y-%m-%d %H:%M:%S %z")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("generated_html", type=Path)
    parser.add_argument("--config", type=Path, default=Path("_config.yml"))
    args = parser.parse_args()

    source = parse_front_matter(args.source)
    config: dict[str, Any] = {}
    for line in args.config.read_text(encoding="utf-8").splitlines():
        if line.startswith(("title:", "url:", "baseurl:")):
            key, _, value = line.partition(":")
            config[key] = parse_scalar(value)

    required = {
        "title",
        "description",
        "excerpt",
        "tags",
        "permalink",
        "last_modified_at",
        "lang",
    }
    missing = sorted(required - source.keys())
    if missing:
        raise ValueError(f"{args.source}: missing fields: {', '.join(missing)}")

    generated = args.generated_html.read_text(encoding="utf-8")
    document = MetadataParser()
    document.feed(generated)
    posting = find_json_ld(document, "BlogPosting")
    find_json_ld(document, "BreadcrumbList")

    tags = source["tags"]
    if not isinstance(tags, list) or not all(tags):
        raise ValueError(f"{args.source}: tags must be a non-empty inline list")
    if not source["excerpt"]:
        raise ValueError(f"{args.source}: excerpt must not be empty")

    site_url = str(config.get("url", "")).rstrip("/")
    baseurl = str(config.get("baseurl", "")).rstrip("/")
    canonical = f"{site_url}{baseurl}{source['permalink']}"
    tag_description = ", ".join(tags)
    errors: list[str] = []

    checks = [
        (source["title"] in document.title, "HTML title does not contain source title"),
        (
            document.meta.get("description") == source["description"],
            "meta description does not match front matter",
        ),
        (document.canonical == canonical, "canonical does not match permalink"),
        (posting.get("url") == canonical, "BlogPosting URL does not match canonical"),
        (
            posting.get("headline") == source["title"],
            "BlogPosting headline does not match title",
        ),
        (
            posting.get("description") == source["description"],
            "BlogPosting description does not match front matter",
        ),
        (
            datetime.fromisoformat(str(posting.get("dateModified")))
            == expected_modified(source),
            "BlogPosting dateModified does not represent last_modified_at",
        ),
        (
            posting.get("inLanguage") == source["lang"],
            "BlogPosting language does not match front matter",
        ),
        (
            all(tag in document.meta.get("keywords", "").split(", ") for tag in tags),
            "generated keywords do not contain every front matter tag",
        ),
        (
            document.meta.get("og:description") == tag_description,
            "OG description does not match the current tag-based template contract",
        ),
        (
            document.meta.get("twitter:description") == tag_description,
            "Twitter description does not match the current tag-based template contract",
        ),
        (
            document.h1_values == [source["title"]],
            "generated HTML must contain exactly one H1 matching title",
        ),
        (
            not source.get("mermaid") or document.has_mermaid_source,
            "mermaid front matter is true but generated diagram source is missing",
        ),
    ]
    for passed, message in checks:
        if not passed:
            errors.append(message)

    if "image" not in source:
        for field in ("og:image", "twitter:image"):
            if field in document.meta:
                errors.append(f"{field} must be absent when front matter has no image")
        if "image" in posting:
            errors.append("BlogPosting image must be absent when front matter has no image")

    if errors:
        for error in errors:
            print(f"FAIL: {error}", file=sys.stderr)
        return 1

    print(
        "PASS: source, title, description, canonical, JSON-LD, tags, excerpt, "
        "keywords, OG/Twitter, H1, image policy, and Mermaid source are consistent"
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        raise SystemExit(1)
