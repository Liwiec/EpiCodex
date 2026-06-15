# EpiCodex

面向流行病学与卫生统计研究的 OpenAI Codex 工作框架。

EpiCodex 把 [EpiClaude](https://github.com/KangWang42/EpiClaude) 的研究工程实践移植到 OpenAI Codex CLI：用一份常驻的 `AGENTS.md` 约束跨会话硬规则，用一组分层的 `skills/` 承载领域能力，从项目初始化、数据分析、发表级绘图、论文写作，到咨询交付与项目审查，形成一条带门禁的可复现流水线。它面向医学研究生、临床数据分析、真实世界数据（Real-World Data, RWD）研究与统计咨询场景。

EpiCodex 不是把 EpiClaude 原样复制，而是按 Codex 的运行机制重写：`CLAUDE.md` → `AGENTS.md`，`settings.json` 钩子 → `config.toml` + 模型自觉遵循，`~/.claude/skills` → `.codex/skills`（由 `SKILL.md` 元数据自动发现）。

## 设计目标

- **规则最小化**：全局规则只保留"删了就会犯具体可观察错误"的硬红线；多步程序性内容下沉到各 skill。
- **治理与流程分离**：`AGENTS.md` 只放跨任务规则与路由指针，具体执行流程写在对应 `SKILL.md`。
- **路由自动化**：任务落入触发场景即自动加载对应 skill，无需用户点名；漏加载视为任务未完成。
- **门禁式状态机**：多步任务统一走 `TODO → PLAN → CODE/WRITE → RUN/RENDER → VERIFY → DOCUMENT`，没有真实运行、渲染或检查前不声明完成。
- **单一数据源**：表图编号由 registry 单源控制；结果数字以 `0_result_summaries.md` 为准；方法决策以 `DECISIONS.md` 为准。
- **零 AI 痕迹**：所有对外产物（论文、报告、表图、代码、交付包）不出现 AI 助手口吻、模板腔、emoji 或"待人工复核"等未完成措辞。

## 五层架构

EpiCodex 的 skill 按"原则层 → 执行层 → 产出层 → 质控层 → 工具层"组织，上层约束下层；多个 skill 同时适用时按此顺序执行。

| 层 | 职责 | 主要 skill |
|---|---|---|
| 原则层 Principle | 底层行为原则、跨 skill 优先级、探索工作流 | `biostat-principles`、`epiclaude-priority`（元路由） |
| 执行层 Execution | 项目脚手架、统计分析、数据清洗 | `project-init`、`r-biostats`（Python 分析沿用同一门禁） |
| 产出层 Output | 发表级图件、论文与投稿材料、汇报、文档格式 | `publication-figures`、`academic-publishing`、`sysu-ppt`、`docx`/`pdf`/`pptx`/`xlsx` |
| 质控层 QC | 项目审查、去 AI 味 | `epi-project-audit`、`humanizer-zh` |
| 工具层 Utility | 咨询交付、中文 IO 健壮性、Git、skill 创建 | `consulting-delivery`、`chinese-io-robustness`、`git-commit-helper`、`skill-creator` |

每一阶段的分析门禁（PLAN-CODE-RUN-VERIFY-DOC）必须走完才能进入下一阶段。统计口径、分组、终点、纳排或主分析方法不明确时，任何层级都先问用户，不自行猜测。

## 核心组件

### 全局治理：`AGENTS.md`

`.codex/AGENTS.md` 是 `CODEX_HOME` 下的常驻全局规则，每个会话都加载。它定义：总体工作方式、自动 skill 路由表、EpiClaude 优先级、研究项目硬规则、运行与自我纠错门禁、交付与写作规范、推荐目录骨架、完成前检查清单。

优先级（冲突时）：系统/开发者指令 > 用户当轮明确指令 > `AGENTS.md` 硬规则 > 项目级 `AGENTS.md`/`CLAUDE.md` > 已加载 skill 流程 > skill 示例与偏好。

### 模块化技能：`skills/`

每个 skill 是一个目录，含 `SKILL.md`（YAML 元数据 `name` + `description` 用于自动发现）与按需加载的 `references/`、`scripts/`、`templates/`。Codex 依据 `description` 中的触发场景决定何时加载，因此描述的精确性直接决定路由质量——重叠 skill 的描述必须互斥并标明优先级，否则会相互抢占。

### 运行配置：`config.toml`

`.codex/config.toml` 设定模型（`gpt-5.5`、推理强度 `xhigh`）、受信项目、沙箱级别、记忆开关与插件。注意：与 EpiClaude 不同，Codex 不通过钩子机械强制规则，硬红线由模型依据 `AGENTS.md` 自觉遵循，因此 `AGENTS.md` 与各 `SKILL.md` 的清晰度尤为关键。

### 记忆：`memories/`

启用 `generate_memories` 与 `use_memories` 后，Codex 跨会话保留项目级事实（如里程碑 commit hash、可回退点、口径决策），用于减少重复试错。

## 技能清单

### EpiClaude 权威技能（优先于同域旧技能）

- `biostat-principles` — 卫生统计/流行病学项目的底层行为原则；所有分析、写作、交付、审查任务开工前先对齐。
- `project-init` — 标准化研究项目初始化：七层目录、模板、Git 配置，支持"研究/咨询"双预设。
- `r-biostats` — R 语言分析执行层：描述统计、回归、生存分析、中介效应、Meta 分析、数据清洗与可视化。
- `publication-figures` — 发表级图件标准 + 约 180 种图类型选型画廊；物理尺寸、字体嵌入、配色、多面板、出图自检。
- `academic-publishing` — 中英双语论文与投稿材料：中文期刊（GB/T 7713）、英文 IMRaD、学位论文，逐部件门控写作。
- `consulting-delivery` — 统计咨询交付包：客户可独立复现、可直接阅读、无 AI 痕迹。
- `epi-project-audit` — 带门禁的六层项目审查状态机：逐项过检、失败给修复建议、全过才签发。
- `humanizer-zh` — 中文文本去 AI 味（润色/改写层），基于困惑度与突发性双杠杆。

### Codex 原生与通用技能

- `docx` / `pdf` / `pptx` / `xlsx` — Office 与 PDF 文件读写、渲染检查。
- `sysu-ppt` — 中山大学学术汇报 PPT（组会 / 开题 / 答辩 / 正式汇报）。
- `chinese-io-robustness` — Windows PowerShell 与 Python 的 UTF-8 安全读写，防中文乱码、路径解析失败与进程卡死。
- `git-commit-helper` — 据 diff 生成描述性提交信息。
- `skill-creator` — 创建与优化 skill。

### 已弃用 / 仅作后备（描述已改为委派，不再就广义任务自动触发）

- `doc` → 改用 `docx`。
- `epi-biostat-consulting` → 拆分为 EpiClaude 分析链（`biostat-principles` → `r-biostats` → `publication-figures` → `academic-publishing` → `consulting-delivery` → `epi-project-audit`）。
- `nature-figure` / `sci-figure` / `paper-figure-style-router` → 仅当用户明确点名某期刊（Nature/SCI/Elsevier 等）视觉样式时使用；常规出图走 `publication-figures`。
- `clinical-public-health-research` → 仅用于 EpiClaude 链未覆盖的英文研究设计 / 评审环节。

### 待补

- `report-writing`（报告类 docx 写作，区别于论文）尚未移植；当前以 `docx` 渲染 + `academic-publishing` 书面语规范 + `humanizer-zh` 暂代。

## 推荐目录骨架

```text
01_data/rawdata/   只读原始数据
02_code/           编号脚本 + config / conventions / lib
03_tables/         Table{N}_*.xlsx；附表进 supplementary/
04_figures/        Fig{N}_*.pdf/png；附图进 supplementary/
05_reports/        咨询或外发交付包
06_results/        中间对象，按内容命名
07_paper/          论文文稿 + 0_result_summaries.md（结果唯一数据源）
09_backup/         旧版、一次性脚本、探索实验
AGENTS.md          项目级规则（如有）
DECISIONS.md       方法与口径决策
SESSION_LOG.md     阶段操作记录
BACKLOG.md         待补清单（发现即记）
```

## 安装与配置

EpiCodex 的全部配置位于 Codex 的 `CODEX_HOME`（本机为 `D:\Codex\.codex`）。

1. 将 `AGENTS.md` 放入 `CODEX_HOME`，作为常驻全局规则。
2. 将各 skill 目录放入 `CODEX_HOME/skills/`，每个目录含 `SKILL.md`（带 `name` + `description` 元数据，供自动发现）。
3. 在 `config.toml` 中设定模型、受信项目、沙箱与记忆开关；保持 skill 路由在 `AGENTS.md` 与各 `SKILL.md`，不要往 `config.toml` 写不受支持的路由键。
4. 可整套部署，也可按需挑选单个 skill。

新建研究项目时调用 `project-init` 一键生成上述目录骨架与模板。

### 安装时的冲突自动停用（硬规则）

将本库 skill 装入使用者的 `CODEX_HOME/skills/` 时，安装代理（Codex）必须执行以下步骤，不等用户点名：

1. **遍历**使用者现有 `skills/` 下每个 `SKILL.md` 的 `description`。
2. **比对**本库即将装入的权威 skill 的触发场景，识别会发生调用冲突的现有 skill——即同一广义触发（如"出图/论文配图""统计分析""写论文"".docx 处理"）会被多个 skill 同时抢占的情况。
3. **直接停用**每个冲突 skill：把其 `SKILL.md` 的 `description` 改写为"已停用 / 委派给 EpiCodex 对应权威 skill"，使其不再就广义任务自动触发。停用以"改写描述、保留文件"为标准做法（可逆）；需硬停用时再将 `SKILL.md` 重命名为 `SKILL.md.disabled`。
4. **不删除、不覆盖**使用者原 skill 的正文内容；只改 `description` 这一路由开关。
5. **登记并汇报**：在安装回复中列出被停用的 skill、判定为冲突的触发词、以及改为委派的目标权威 skill，供使用者复核。

判定冲突的优先级固定：EpiCodex 的 EpiClaude 权威 skill 为准，使用者侧同域旧 skill 一律降级为后备。本规则同时写入 `AGENTS.md`，确保每个会话都生效。

## 发布到 GitHub：上传清单

要让下载者完美复刻 EpiClaude，上传"全局规则 + EpiClaude 权威技能 + 钩子 + 脱敏配置模板"，排除会引发冲突的旧技能、Anthropic 专有技能与含本机隐私的运行配置。本仓库（`D:\Claude\lib1\EpiCodex`）已按此清单整理完毕。

**必传（复刻核心，本仓库已含）**

- `README.md`、`AGENTS.md`（`CLAUDE.md` 的 Codex 对等物，全局常驻规则与路由表）、`config.toml.example`（脱敏配置 + 钩子配线）。
- `hooks/` —— 6 个 Python 钩子 + `_hooklib.py`，把硬红线升级为框架机械强制（见下文"相对 EpiClaude 的改动"）。
- EpiClaude 权威 skill（10 个）：`biostat-principles`、`project-init`、`r-biostats`、`publication-figures`、`academic-publishing`、`consulting-delivery`、`epi-project-audit`、`humanizer-zh`、`report-writing`、`sysu-ppt`。
- Codex 专属增强（2 个）：`epiclaude-priority`（无内置路由强制时用此元路由表达"EpiClaude 优先"）、`chinese-io-robustness`（Windows + PowerShell 的 UTF-8 安全 IO）。
- `git-commit-helper` —— 轻量、无专有许可，一并附带。

**不要上传（专有 / 会引发冲突 / 含隐私）**

- Anthropic 专有技能：`docx`、`pdf`、`pptx`、`xlsx`、`skill-creator`——其 `SKILL.md` 标注 `license: Proprietary`，随 Codex / Claude 一并分发，**不得再上传到公共仓库**；下载者本机已自带。
- 旧/重复 skill：`doc`、`epi-biostat-consulting`、`nature-figure`、`sci-figure`、`paper-figure-style-router`、`clinical-public-health-research`——它们正是冲突源，上传会破坏复刻。
- `config.toml`、`auth.json`、`memories/`、`sessions/`、`.sandbox*`、各 `*.sqlite`、插件运行时缓存——含本机绝对路径、鉴权、受信项目与会话隐私。只提供脱敏的 `config.toml.example`。

**关于钩子（更正早期说法）**：Codex CLI **支持钩子**，事件名（PreToolUse / PostToolUse / Stop 等）、stdin JSON 输入、`permissionDecision:"deny"` 与 exit 2 反馈的 schema 与 Claude Code 基本一致。EpiClaude 的钩子因此可以复刻——唯一差异是 Codex 的工具模型是 `apply_patch` / `Bash`（而非 `Write/Edit/MultiEdit`），故 `matcher` 与路径解析已相应改写。仅需留意 Codex 个别版本/桌面端存在"钩子不运行"的已知问题（[openai/codex#21639](https://github.com/openai/codex/issues/21639)），安装后建议实测一次。

## 设计哲学

- **规则过"删除测试"**：每条全局规则都要满足"删了 Claude/Codex 会犯具体可观察的错误"才保留，目标全局规则 < 120 行。
- **渐进式披露**：模板与参考资料按需进入上下文，避免一次性塞满。
- **可复现优先**：对外交付物自带代码、输入说明、环境说明、结果与运行顺序，他人可独立复现。
- **数据缺陷不擅自写进交付物**：发现缺失/需反推/口径不全先回原始数据与权威源核实、向用户汇报、记入 `BACKLOG.md`，能补则补，补不全才与用户商定表述。
- **领域可迁移**：技能内容面向流行病学，但底层研究工程实践（分层组织、状态机、单一数据源、发表标准、零 AI 痕迹）同样适用于其他定量研究领域。

## 致谢

本框架的架构与规则体系参照 [EpiClaude](https://github.com/KangWang42/EpiClaude)（作者 KangWang42），并按 OpenAI Codex 的运行机制重写。原作把流行病学研究工程的分层治理、状态机门禁、单一数据源与零 AI 痕迹标准沉淀成一套可复用的体系，本项目得以站在其肩上。

## 相对 EpiClaude 的改动 / Changes relative to EpiClaude

EpiCodex 不是逐字搬运，而是按 Codex 的运行机制做了适配与取舍。主要差异如下。

**1. 治理载体：`CLAUDE.md` → `AGENTS.md`**
全局常驻规则改写为 Codex 读取的 `AGENTS.md`，保留 EpiClaude 的路由表、硬红线与完成前检查，并新增"EpiClaude 优先级"与"已弃用 skill 委派"说明。

**2. 钩子：bash + Write/Edit/MultiEdit → Python + apply_patch/Bash**
EpiClaude 的 6 个 bash 钩子针对 Claude Code 的 `Write/Edit/MultiEdit` 工具、从 `tool_input.file_path` 取路径。EpiCodex 全部改写为 **Python**（兼容 Windows，无需 bash），并适配 Codex 工具模型：`matcher` 改为 `apply_patch` / `Bash`，路径解析改为从 `apply_patch` 补丁头与 `Bash` 命令中提取（公共逻辑下沉 `_hooklib.py`）。`deny` JSON 与 exit 2 反馈协议与原作一致。状态文件位置由 `~/.claude` 改到 `CODEX_HOME`。

**3. 新增"安装时冲突自动停用"硬规则**
针对 Codex 用户机器上常并存大量旧 skill 的现实，新增一条 EpiClaude 没有的规则：安装本框架时自动遍历使用者现有 `SKILL.md`，把会和权威 skill 抢占同一广义触发的旧 skill 就地降级为委派（改 `description`、保留文件，可逆），并登记汇报。

**4. 路由委派而非删除：处理 Codex 侧的历史重复 skill**
Codex 安装里原本散落 `doc` / `epi-biostat-consulting` / `nature-figure` / `sci-figure` / `paper-figure-style-router` / `clinical-public-health-research` 等与权威 skill 冲突的旧技能。EpiCodex 将它们的 `description` 改为"已停用/委派"，使自动路由只命中权威 skill；并修复了 `sci-figure` 缺失 YAML 元数据、无法被发现的问题。

**5. 新增 Codex 专属增强 skill**
`epiclaude-priority`（Codex 无内置 CLAUDE.md 级优先级时，用元路由 skill 表达"EpiClaude 权威"）与 `chinese-io-robustness`（Windows + PowerShell 的 UTF-8 安全 IO，防中文乱码/路径失败）为 EpiClaude 所无。

**6. 配置形态：`settings.json` 片段 → `config.toml.example`**
EpiClaude 用 `settings.json` 片段挂钩子；EpiCodex 改为 `config.toml` 的 `[[hooks.*]]` 数组表，并提供一份脱敏 `config.toml.example`（去除本机路径、鉴权、MCP 运行时与受信项目）。

**7. 不再分发 Anthropic 专有技能**
`docx` / `pdf` / `pptx` / `xlsx` / `skill-creator` 标注专有许可，随 Codex / Claude 自带，故本仓库不收录、不再分发（EpiClaude 同理）。

**已知差异与局限 / Known gap**：Codex 个别版本或桌面端存在钩子不触发的问题（[openai/codex#21639](https://github.com/openai/codex/issues/21639)）。若钩子未运行，硬红线会退回"模型依据 `AGENTS.md` 自觉遵循"，强度低于机械强制——安装后请按 `hooks/README.md` 实测一次确认钩子生效。

## 贡献者 / Contributors

- **原始框架 / Original framework**：[KangWang42](https://github.com/KangWang42) —— [EpiClaude](https://github.com/KangWang42/EpiClaude)。
- **Codex 移植与维护 / Codex port & maintenance**：[Liwiec](https://github.com/Liwiec)。
- **协作开发 / Co-developed with**：Claude（Anthropic Claude Code, Opus 4.8）—— 完成钩子移植、skill 路由去冲突、仓库整理与本文档撰写。
