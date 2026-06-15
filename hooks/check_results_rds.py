#!/usr/bin/env python
# PostToolUse(Bash)：检测 06_results/ 新写入的 .rds，提醒"表格化数据应存 xlsx，rds 仅限非表格对象"。
# 对照 EpiClaude check_results_rds.sh。状态文件改放 CODEX_HOME（原放 ~/.claude）。
import os
import time
import _hooklib as h

d = h.load()
h.chdir_cwd(d)
if not os.path.isdir("06_results"):
    h.ok()

state = h.state_path(".rds_reminded")
seen = set()
if os.path.exists(state):
    try:
        seen = set(open(state, encoding="utf-8").read().splitlines())
    except Exception:
        seen = set()

now = time.time()
new_keys, flagged = [], []
for root, _dirs, files in os.walk("06_results"):
    for fn in files:
        if not fn.lower().endswith(".rds"):
            continue
        fp = os.path.join(root, fn)
        try:
            mt = int(os.path.getmtime(fp))
        except OSError:
            continue
        if now - mt > 120:  # 仅近 120 秒新写入
            continue
        key = f"{fp}|{mt}"
        if key in seen:
            continue
        new_keys.append(key)
        flagged.append(fp.replace("\\", "/"))

if new_keys:
    try:
        os.makedirs(os.path.dirname(state), exist_ok=True)
        with open(state, "a", encoding="utf-8") as fh:
            for k in new_keys:
                fh.write(k + "\n")
    except Exception:
        pass

if flagged:
    msg = ("检测到 06_results/ 新写入 .rds：\n"
           + "\n".join("  · " + f for f in flagged)
           + "\n→ 仅非表格对象（拟合模型 / ggplot / MCA 等）可用 rds；"
             "表格化数据必须存 .xlsx（writexl::write_xlsx）。若上述是表格，请改存 xlsx。")
    h.feedback(msg)
h.ok()
