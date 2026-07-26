#!/usr/bin/env python3
"""Acquire and release the local singleton lease for notion-run-queue."""

from __future__ import annotations

import argparse
import json
import os
import re
import socket
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

RUN_ID_RE = re.compile(r"^[A-Za-z0-9._:-]{1,128}$")
LOCK_NAME = "notion-run-queue.lock"
OWNER_NAME = "owner.json"


def git_common_dir(repo: Path) -> Path:
    result = subprocess.run(
        [
            "git",
            "-C",
            str(repo),
            "rev-parse",
            "--path-format=absolute",
            "--git-common-dir",
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    return Path(result.stdout.strip()).resolve()


def lease_paths(repo: Path) -> tuple[Path, Path]:
    common_dir = git_common_dir(repo)
    lock_dir = common_dir / "codex" / LOCK_NAME
    return lock_dir, lock_dir / OWNER_NAME


def read_owner(owner_path: Path) -> dict[str, object] | None:
    try:
        return json.loads(owner_path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def print_json(payload: dict[str, object]) -> None:
    print(json.dumps(payload, ensure_ascii=False, sort_keys=True))


def validate_run_id(run_id: str) -> None:
    if not RUN_ID_RE.fullmatch(run_id):
        raise ValueError(
            "run-id must be 1-128 characters using letters, digits, '.', '_', ':', or '-'"
        )


def acquire(repo: Path, run_id: str) -> int:
    validate_run_id(run_id)
    lock_dir, owner_path = lease_paths(repo)
    lock_dir.parent.mkdir(parents=True, exist_ok=True)

    try:
        os.mkdir(lock_dir)
    except FileExistsError:
        print_json(
            {
                "status": "busy",
                "lock_dir": str(lock_dir),
                "owner": read_owner(owner_path),
            }
        )
        return 2

    owner = {
        "run_id": run_id,
        "pid": os.getpid(),
        "host": socket.gethostname(),
        "acquired_at": datetime.now(timezone.utc).isoformat(),
        "repo": str(repo.resolve()),
    }

    try:
        with owner_path.open("x", encoding="utf-8") as file:
            json.dump(owner, file, ensure_ascii=False, sort_keys=True)
            file.write("\n")
    except Exception:
        os.rmdir(lock_dir)
        raise

    print_json({"status": "acquired", "lock_dir": str(lock_dir), "owner": owner})
    return 0


def status(repo: Path) -> int:
    lock_dir, owner_path = lease_paths(repo)
    if not lock_dir.exists():
        print_json({"status": "free", "lock_dir": str(lock_dir)})
        return 0

    print_json(
        {
            "status": "busy",
            "lock_dir": str(lock_dir),
            "owner": read_owner(owner_path),
        }
    )
    return 2


def release(repo: Path, run_id: str) -> int:
    validate_run_id(run_id)
    lock_dir, owner_path = lease_paths(repo)
    owner = read_owner(owner_path)

    if owner is None:
        print_json(
            {
                "status": "release_refused",
                "reason": "missing or invalid owner record",
                "lock_dir": str(lock_dir),
            }
        )
        return 3

    if owner.get("run_id") != run_id:
        print_json(
            {
                "status": "release_refused",
                "reason": "run-id does not own the lease",
                "lock_dir": str(lock_dir),
                "owner": owner,
            }
        )
        return 3

    unexpected = [path.name for path in lock_dir.iterdir() if path.name != OWNER_NAME]
    if unexpected:
        print_json(
            {
                "status": "release_refused",
                "reason": "unexpected files in lease directory",
                "lock_dir": str(lock_dir),
                "unexpected": sorted(unexpected),
            }
        )
        return 3

    owner_path.unlink()
    os.rmdir(lock_dir)
    print_json({"status": "released", "lock_dir": str(lock_dir), "run_id": run_id})
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("acquire", "status", "release"))
    parser.add_argument("--repo", required=True, type=Path)
    parser.add_argument("--run-id")
    args = parser.parse_args()

    if args.command in {"acquire", "release"} and not args.run_id:
        parser.error(f"{args.command} requires --run-id")

    try:
        if args.command == "acquire":
            return acquire(args.repo, args.run_id)
        if args.command == "release":
            return release(args.repo, args.run_id)
        return status(args.repo)
    except (ValueError, subprocess.CalledProcessError, OSError) as error:
        print_json({"status": "error", "error": str(error)})
        return 1


if __name__ == "__main__":
    sys.exit(main())
