#!/usr/bin/env python
from __future__ import annotations

import argparse
import shutil
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


def decode_text(path: Path) -> tuple[str, str]:
    for enc in ("utf-8-sig", "utf-8", "gb18030", "utf-16"):
        try:
            return path.read_text(encoding=enc), enc
        except UnicodeDecodeError:
            continue
    raise UnicodeDecodeError("unknown", b"", 0, 1, f"cannot decode {path}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Mirror folder with UTF-8 normalized text files.")
    parser.add_argument("src", help="Source root")
    parser.add_argument("dst", help="Destination root")
    args = parser.parse_args()

    src = Path(args.src)
    dst = Path(args.dst)
    if not src.exists():
        print(f"[ERROR] source does not exist: {src}")
        return 2
    dst.mkdir(parents=True, exist_ok=True)

    total = 0
    repaired = 0
    failed: list[Path] = []
    for p in src.rglob("*"):
        rel = p.relative_to(src)
        out = dst / rel
        if p.is_dir():
            out.mkdir(parents=True, exist_ok=True)
            continue

        total += 1
        out.parent.mkdir(parents=True, exist_ok=True)
        ext = p.suffix.lower()
        if ext not in TEXT_EXTS:
            shutil.copy2(p, out)
            continue

        try:
            text, enc = decode_text(p)
            out.write_text(text, encoding="utf-8", newline="")
            if enc != "utf-8":
                repaired += 1
        except Exception:
            failed.append(p)
            shutil.copy2(p, out)

        if total % 200 == 0:
            print(f"[PROGRESS] processed={total} repaired={repaired} failed={len(failed)}")

    print(f"[SUMMARY] processed={total} repaired={repaired} failed={len(failed)}")
    if failed:
        print("[FAILED_FILES]")
        for f in failed:
            print(str(f))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

