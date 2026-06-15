"""EpiCodex 钩子公共库 / Shared library for EpiCodex hooks.

适配 Codex 的工具模型：文件编辑走 apply_patch（补丁字符串），命令走 Bash。
Codex 把单个 JSON 对象交给钩子的 stdin，字段含 tool_name / tool_input / tool_response / cwd。
对照 EpiClaude 的 _resolve_path.sh（读 tool_input.file_path，针对 Write/Edit/MultiEdit）。

Adapts to Codex's tool model: file edits via apply_patch (patch text), commands via Bash.
Codex passes one JSON object on the hook's stdin with tool_name / tool_input / tool_response / cwd.
"""
import sys
import os
import re
import json


def load():
    """读取 Codex 交给 stdin 的钩子 JSON。/ Read the hook JSON Codex sends on stdin."""
    try:
        return json.load(sys.stdin)
    except Exception:
        return {}


def tool_name(d):
    return d.get("tool_name") or ""


def cwd(d):
    return d.get("cwd") or ""


def chdir_cwd(d):
    """切到 Codex 提供的工作目录，便于按相对路径找 06_results/04_figures 等。"""
    c = cwd(d)
    if c:
        try:
            os.chdir(c)
        except Exception:
            pass


_PATCH_FILE = re.compile(r"\*\*\*\s+(?:Update|Add|Delete) File:\s+(.+)")


def changed_paths(d):
    """提取本次工具调用涉及的文件路径。
    apply_patch：从补丁头 `*** Update/Add/Delete File:` 解析；
    其它工具/MCP：尽量从 file_path / path 字段取。反斜杠归一为正斜杠。
    """
    ti = d.get("tool_input")
    tr = d.get("tool_response") if isinstance(d.get("tool_response"), dict) else {}
    out = []
    blob = ""
    if isinstance(ti, dict):
        for k in ("file_path", "path"):
            v = ti.get(k) or tr.get(k)
            if v:
                out.append(v)
        for k in ("input", "patch", "content"):
            v = ti.get(k)
            if isinstance(v, str):
                blob += "\n" + v
    elif isinstance(ti, str):
        blob = ti
    for m in _PATCH_FILE.findall(blob):
        out.append(m.strip())
    seen, res = set(), []
    for p in out:
        p = p.replace("\\", "/").strip().strip('"')
        if p and p not in seen:
            seen.add(p)
            res.append(p)
    return res


def command_str(d):
    """取 Bash 工具的命令字符串。/ Get the Bash tool command string."""
    ti = d.get("tool_input")
    if isinstance(ti, dict):
        c = ti.get("command")
        if isinstance(c, list):
            return " ".join(str(x) for x in c)
        if isinstance(c, str):
            return c
    return ""


def state_path(name):
    """钩子状态文件路径（放 CODEX_HOME，对照 EpiClaude 放 ~/.claude）。"""
    home = os.environ.get("CODEX_HOME") or os.path.join(os.path.expanduser("~"), ".codex")
    return os.path.join(home, name)


def deny(reason, event="PreToolUse"):
    """PreToolUse 拒绝：与 Codex / Claude Code 同一 JSON schema。"""
    sys.stdout.write(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": event,
            "permissionDecision": "deny",
            "permissionDecisionReason": reason,
        }
    }) + "\n")
    sys.exit(0)


def feedback(msg):
    """把信息反馈给模型：stderr + exit 2（Codex 会以此替换工具结果并续跑）。"""
    sys.stderr.write(msg + "\n")
    sys.exit(2)


def ok():
    sys.exit(0)
