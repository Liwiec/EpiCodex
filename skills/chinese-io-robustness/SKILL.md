---
name: chinese-io-robustness
description: Use when file paths, file names, or file contents include Chinese characters and workflows risk encoding errors, mojibake, or process hangs. Enforces end-to-end UTF-8 safe execution on Windows PowerShell and Python without skipping files.
---

# Chinese IO Robustness

Use this skill for any task that involves Chinese directories, Chinese file names, or Chinese text content.

Goal: complete the full workflow without stalls, path failures, or garbled output.

## Activation Signals

Apply this skill immediately when any of these appear:
- Non-ASCII path segments (for example Chinese folder names).
- Console errors mentioning encoding, decode, unicode, cp936, gbk, gb18030, mojibake, or unreadable characters.
- Scripts that read/write many text files and may silently skip failures.

## Mandatory Execution Protocol

1. Run preflight environment setup first.
2. Probe paths and text decode before heavy processing.
3. Normalize problematic text encodings to UTF-8 in a mirrored workspace.
4. Execute pipeline against normalized paths/files when needed.
5. Run post-checks to confirm no skipped files and no replacement characters.

Never bypass unreadable files. Repair then continue.

## Step 1: PowerShell UTF-8 Preflight

Set these before running file-heavy commands:

```powershell
[Console]::InputEncoding = [System.Text.UTF8Encoding]::new($false)
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new($false)
$OutputEncoding = [System.Text.UTF8Encoding]::new($false)
$PSDefaultParameterValues['*:Encoding'] = 'utf8'
$env:PYTHONUTF8 = '1'
$env:PYTHONIOENCODING = 'utf-8'
```

Important:
- Do not rely only on PowerShell profile settings. Some agent runtimes call PowerShell with `-NoProfile`.
- If shell is re-invoked per command, prepend the UTF-8 preflight in the same command block that performs file IO.
- Verify active code page and encoding when debugging:
  - `chcp`
  - `[Console]::OutputEncoding.WebName`

Then prefer:
- `Get-ChildItem -LiteralPath ...`
- `Get-Content -LiteralPath ... -Encoding utf8`
- `Set-Content -LiteralPath ... -Encoding utf8`

Use `-LiteralPath` for all user-provided paths to avoid wildcard/path parsing issues.

## Step 2: Path and Decode Probe

Before the main task:
- Run `scripts/path_probe.py` to count files and test openability.
- If decode failures occur, run `scripts/normalize_to_utf8.py` and continue from the normalized mirror folder.

## Step 3: Python IO Rules (Strict)

In custom Python code:
- Always use `pathlib.Path`.
- Always pass explicit `encoding='utf-8'` for writes.
- For unknown text input, try deterministic fallback order:
  1. `utf-8-sig`
  2. `utf-8`
  3. `gb18030`
  4. `utf-16`
- If all fail, stop and report exact file path and bytes offset. Do not skip silently.

## Step 4: Anti-Stall Rules

- For long loops, print periodic progress every N files.
- Use bounded retry (`max 2`) for transient file locks.
- If a file blocks progress, move it to a repair queue and continue, then process queue before finishing.
- Final status is success only when repair queue is empty.

## Step 5: Completion Checks

Must satisfy all:
- Input and processed file counts reconcile (or documented expected exclusions).
- No `UnicodeDecodeError`/`UnicodeEncodeError` in logs.
- No mojibake markers (`�`) in outputs.
- Chinese paths and text render correctly in final artifacts.

## References

- [Execution checklist](references/execution-checklist.md)
- [PowerShell patterns](references/powershell-patterns.md)

## Scripts

- `scripts/path_probe.py`
- `scripts/normalize_to_utf8.py`
