#!/usr/bin/env python
from __future__ import annotations

import argparse
from pathlib import Path


TEXT_EXTS = {
    ".txt",
    ".csv",
    ".tsv",
    ".md",
    ".json",
    ".yaml",
    ".yml",
    ".log",
    ".r",
    ".py",
    ".do",
    ".sas",
    ".sql",
}


def decode_probe(path: Path) -> tuple[bool, str]:
    if path.suffix.lower() not in TEXT_EXTS:
        return True, "binary-or-ignored"
    for enc in ("utf-8-sig", "utf-8", "gb18030", "utf-16"):
        try:
            path.read_text(encoding=enc)
            return True, enc
        except UnicodeDecodeError:
            continue
    return False, "decode-failed"


def main() -> int:
    parser = argparse.ArgumentParser(description="Probe paths and decodability.")
    parser.add_argument("root", help="Root folder to scan")
    args = parser.parse_args()

    root = Path(args.root)
    if not root.exists():
        print(f"[ERROR] root does not exist: {root}")
        return 2

    files = [p for p in root.rglob("*") if p.is_file()]
    failed: list[Path] = []
    for idx, f in enumerate(files, start=1):
        ok, reason = decode_probe(f)
        if not ok:
            failed.append(f)
        if idx % 200 == 0:
            print(f"[PROGRESS] checked={idx} failed={len(failed)}")

    print(f"[SUMMARY] total_files={len(files)} decode_failed={len(failed)}")
    if failed:
        print("[FAILED_FILES]")
        for p in failed:
            print(str(p))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

