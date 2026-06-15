#!/usr/bin/env python
# PostToolUse(Bash)：检测 04_figures/ 新生成或修改的图 → 注入 publication-figures 逐元素自检清单，
# 逼主模型 Read 该图逐条判断。钩子不做视觉判断（命令看不了图），只负责"逮住出图事件 + 强制自检"。
# 对照 EpiClaude fig_selfcheck.sh。状态文件改放 CODEX_HOME（原放 ~/.claude）。
import os
import time
import _hooklib as h

d = h.load()
h.chdir_cwd(d)
if not os.path.isdir("04_figures"):
    h.ok()

state = h.state_path(".fig_selfcheck_state")
seen = []
if os.path.exists(state):
    try:
        seen = open(state, encoding="utf-8").read().splitlines()
    except Exception:
        seen = []
seen_set = set(seen)

now = time.time()
new_keys, new_imgs = [], []
for root, _dirs, files in os.walk("04_figures"):
    for fn in files:
        if not fn.lower().endswith((".png", ".pdf")):
            continue
        fp = os.path.join(root, fn)
        try:
            mt = int(os.path.getmtime(fp))
        except OSError:
            continue
        if now - mt > 120:
            continue
        key = f"{fp}|{mt}"
        if key in seen_set:
            continue
        new_keys.append(key)
        new_imgs.append(fp.replace("\\", "/"))

if new_keys:
    try:
        os.makedirs(os.path.dirname(state), exist_ok=True)
        combined = seen + new_keys
        if len(combined) > 600:  # 控制状态文件大小
            combined = combined[-300:]
        with open(state, "w", encoding="utf-8") as fh:
            fh.write("\n".join(combined) + "\n")
    except Exception:
        pass

if new_imgs:
    msg = ("检测到新生成/修改的图，按 publication-figures 逐项自检"
           "（先 Read 该 PNG/PDF，逐条判，任一不过=回代码层改重出）：\n"
           + "\n".join("  · " + f for f in new_imgs) + "\n"
           "① 图例/标签/注释不遮挡任何数据（线/点/柱/误差棒）；遮挡即不合格\n"
           "② 比例尺寸合适，无大片空边、无元素被裁切（轴/标题/图例/刻度完整）\n"
           "③ 每个元素清晰可读（嵌入尺寸下字号够大）\n"
           "④ 数值可溯源不硬编码、与 results.yaml 一致；无统计假象（全同值/恒 ±0.707 等）\n"
           "⑤ 图型匹配数据、与同篇其它图 theme/配色/布局一致、多结局不漏")
    h.feedback(msg)
h.ok()
