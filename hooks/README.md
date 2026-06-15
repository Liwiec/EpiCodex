# EpiCodex 钩子 / Hooks

把 EpiClaude 的硬红线从"模型自觉"升级为"框架机械强制"。对照 EpiClaude `hooks/`（bash，针对 Claude Code 的 Write/Edit/MultiEdit），本目录改写为 **Python + Codex 工具模型（apply_patch / Bash）**，以兼容 Windows。

These reproduce EpiClaude's mechanically-enforced red lines on Codex. Rewritten in Python and adapted to Codex's tool model (apply_patch / Bash) for Windows compatibility.

## 脚本 / Scripts

| 脚本 | 事件 / matcher | 作用 |
|---|---|---|
| `protect_rawdata.py` | PreToolUse(apply_patch\|Bash) | 拦截对 `01_data/rawdata/` 的修改，`deny` |
| `scan_ai_trace.py` | PostToolUse(apply_patch) | 扫文本里的 AI 痕迹字样与 emoji（放过 ✅），命中 exit 2 反馈 |
| `check_r_syntax.py` | PostToolUse(apply_patch) | 对改动的 `.R` 跑 `Rscript` parse，语法错 exit 2；无 R 环境则跳过 |
| `check_results_rds.py` | PostToolUse(Bash) | 检测 `06_results/` 近 120 秒新写入的 `.rds`，提醒表格化数据应存 xlsx |
| `fig_selfcheck.py` | PostToolUse(Bash) | 检测 `04_figures/` 新图，注入逐元素自检清单逼模型 Read 该图复核 |
| `_hooklib.py` | （公共库） | 解析 Codex stdin JSON：`tool_name` / `cwd` / 受影响文件路径 / 命令串 |

## 安装 / Install

1. 把本目录拷到 `CODEX_HOME/hooks/`（如 `D:\Codex\.codex\hooks\`）。
2. 把 `../config.toml.example` 里的 `[[hooks.*]]` 段并入你的 `CODEX_HOME/config.toml`，把 `<CODEX_HOME>` 换成实际路径。
3. 需要 `python` 在 PATH 上；`check_r_syntax.py` 额外需要 `Rscript`（缺则自动跳过）。

## 注意 / Caveat

Codex 部分版本/桌面端存在"钩子不运行"的已知问题（见 openai/codex#21639）。安装后请实测一次：故意编辑一个含 emoji 的 `.md`，确认收到 PostToolUse 反馈。

Some Codex versions/desktop builds have a known "hooks not running" issue (openai/codex#21639). After install, verify once by editing a `.md` containing an emoji and confirming the PostToolUse feedback fires.
