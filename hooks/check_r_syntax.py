#!/usr/bin/env python
# PostToolUse(apply_patch)：对 .R 文件做语法 parse 检查，出错即反馈给模型（exit 2）。
# 对照 EpiClaude check_r_syntax.sh（针对 Write|Edit|MultiEdit）。无 R 环境则跳过、不阻断。
import os
import subprocess
import _hooklib as h

d = h.load()
h.chdir_cwd(d)
bad = []
for p in h.changed_paths(d):
    if not p.lower().endswith(".r"):
        continue
    if not os.path.exists(p):  # 文件不存在（如纯删除补丁）跳过
        continue
    try:
        r = subprocess.run(
            ["Rscript", "-e", "invisible(parse(commandArgs(TRUE)[1]))", p],
            capture_output=True, text=True)
    except FileNotFoundError:
        h.ok()  # 本机无 R，跳过
    if r.returncode != 0:
        bad.append(f"R 语法检查未过 ({p})：\n{(r.stderr or r.stdout).strip()}")

if bad:
    h.feedback("\n".join(bad))
h.ok()
