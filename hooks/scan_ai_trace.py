#!/usr/bin/env python
# PostToolUse(apply_patch)：扫文本文件里的 emoji 与 AI 痕迹字样，命中反馈给模型（exit 2）。
# 放过 ✅（BACKLOG 约定状态标记）；跳过 .codex/ 下的 skill/配置文件（它们合法地讨论这些字样）。
# 对照 EpiClaude scan_ai_trace.sh（针对 Write|Edit|MultiEdit，跳过 .claude/）。
import _hooklib as h
import re

AI = re.compile(r"AI辅助|AI_assisted|AI-assisted|机辅|机器辅助|待人工复核|AI ?生成|机辅待核")
EMOJI = re.compile("[\U0001F300-\U0001FAFF☀-➿⬀-⯿←-⇿]")
CHECK = "✅"  # ✅ BACKLOG 状态标记，放过
EXTS = (".md", ".r", ".txt", ".csv", ".yaml", ".yml", ".py")

d = h.load()
h.chdir_cwd(d)
problems = []
for p in h.changed_paths(d):
    if "/.codex/" in p or p.startswith(".codex/"):
        continue
    if not p.lower().endswith(EXTS):
        continue
    try:
        with open(p, encoding="utf-8", errors="ignore") as fh:
            lines = fh.readlines()
    except Exception:
        continue
    for i, line in enumerate(lines, 1):
        if AI.search(line):
            problems.append(f"[AI痕迹] {p}:{i}: {line.rstrip()}")
        for m in EMOJI.finditer(line):
            if m.group(0) != CHECK:
                problems.append(f"[emoji] {p}:{i}: {line.rstrip()}")
                break

if problems:
    h.feedback("检测到 AI 痕迹 / emoji（工作产物需清除，✅ 状态标记除外）：\n" + "\n".join(problems))
h.ok()
