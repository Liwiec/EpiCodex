#!/usr/bin/env python
# PreToolUse(apply_patch|Bash)：拦截对 01_data/rawdata 原始数据的修改（AGENTS.md 红线）。
# 对照 EpiClaude protect_rawdata.sh（针对 Write|Edit|MultiEdit）。Codex 改编：
#   - apply_patch：从补丁头解析目标文件，命中 rawdata 即 deny；
#   - Bash：命令同时提到 rawdata 且含写操作（重定向/rm/mv/cp/tee/dd/saveRDS/write_*）才 deny，避免误伤只读。
import re
import _hooklib as h

d = h.load()
hits = [p for p in h.changed_paths(d)
        if re.search(r"(^|/)01_data/rawdata/|(^|/)rawdata/", p)]

cmd = h.command_str(d)
if re.search(r"rawdata", cmd) and re.search(
        r"(>>?|\brm\b|\bmv\b|\bcp\b|\btee\b|\bdd\b|saveRDS|write\.|write_xlsx|writexl)", cmd):
    hits.append("(bash 命令疑似写入 rawdata)")

if hits:
    h.deny("01_data/rawdata 是只读原始数据，禁止修改（AGENTS.md 红线）。"
           "如确需变更请改派生数据或先与用户确认。命中：" + "; ".join(hits))
h.ok()
