# Codex 全局规则：流行病学 / 卫生统计 / 学术交付

本文件是 `D:\Codex\.codex` 下的全局常驻规则，用于把 EpiClaude 的 `CLAUDE.md` 路由逻辑改写为 Codex 可执行的 `AGENTS.md` 规则。它不覆盖系统/开发者指令，也不覆盖用户当轮明确要求；当发生冲突时，优先级为：系统/开发者指令 > 用户当轮明确指令 > 本文件硬规则 > 项目级 AGENTS.md/CLAUDE.md > 已加载 skill 流程 > skill 示例和偏好。

## 1. 总体工作方式

- 面向卫生统计、流行病学、公共卫生、临床研究、统计咨询、论文写作和科研绘图任务时，默认采用 EpiClaude 工作流。
- 任务进入执行阶段前，先判断是否需要调用对应 Codex skill；只要触发场景匹配，就主动加载并遵循对应 `SKILL.md`，不等待用户点名。
- 多步骤任务使用 `TODO -> PLAN -> CODE/WRITE -> RUN/RENDER -> VERIFY -> DOCUMENT` 状态机；没有真实运行、渲染或检查前，不声明完成。
- 遇到分组、终点、纳排、主分析方法、统计口径或交付对象不明确时，先问用户；不要自行猜测关键研究口径。
- 写作和交付文本使用研究者/咨询者视角，避免 AI 助手口吻、模板腔、宣传腔和不必要的寒暄。
- 不猜 API、包版本、数据结构或文件内容；先读文件、代码、日志或官方文档，再给结论。
- 涉及中文路径、中文文件名或中文内容时，必须按 `chinese-io-robustness` 执行 UTF-8 安全读取/写入；不允许因中文乱码、路径解析失败而跳过文件。

## 2. 自动 skill 路由

| 触发场景 | 优先调用的 Codex skill |
|---|---|
| 流行病学、卫生统计、公共卫生、临床研究、统计咨询、论文、投稿、去 AI 味、发表级图表 | `epiclaude-priority` |
| 新建研究项目、初始化目录、建立可复现项目结构 | `project-init`，并先对齐 `biostat-principles` |
| R 统计分析、描述统计、回归、生存分析、中介效应、Meta 分析、数据清洗、R 可视化 | `biostat-principles` -> `r-biostats` |
| Python 统计分析或清洗 | `biostat-principles`；沿用 EpiClaude 的 PLAN-CODE-RUN-VERIFY-DOC 门禁，并使用项目内 Python 工具链 |
| 任意科研出图、论文配图、ggplot、matplotlib、森林图、热图、生存曲线、图表配色 | `publication-figures`；除非用户明确指定，否则优先于 `nature-figure` / `sci-figure` / `paper-figure-style-router` |
| 写作或修改论文任一部分、摘要、方法、结果、讨论、投稿信、审稿回复、Highlights、Graphical Abstract | `biostat-principles` -> `academic-publishing`；中文最终稿再过 `humanizer-zh` |
| 中文润色、去 AI 味、文风更像研究者、报告或论文语言自然化 | `humanizer-zh` |
| 给客户做统计咨询、打包分析结果、外发代码和结果、要求别人可复现 | `biostat-principles` -> `consulting-delivery` |
| 项目审查、质控、复核结果、检查代码/表图/论文数字一致性 | `biostat-principles` -> `epi-project-audit` |
| 尝试新方法、优化模型、前沿方法、探索性分析 | `biostat-principles` 的隔离探索工作流 |
| Word/docx、PDF、PPTX、XLSX 文件处理 | 优先使用 EpiClaude 对应 `docx` / `pdf` / `pptx` / `xlsx`；如插件工具更适合渲染检查，可结合 Documents/Presentations/Spreadsheets 插件 |
| 写作或修改报告类 docx（分析报告 / 进展 / 说明 / 指南 / 手册 / 备忘，非论文非投稿） | 暂无专用 report-writing skill：用 `docx` 渲染落地，写作沿用 `academic-publishing` 的书面语与零 AI 痕迹规范，中文终稿过 `humanizer-zh` |
| 中山大学组会汇报或医学组会 PPT | `sysu-ppt` |
| Git 提交信息、阶段性变更摘要 | `git-commit-helper` |

路由规则是自动义务：任务明显落入上表时，第一步加载对应 skill；漏加载视为任务未完成。若多个 skill 同时适用，按“原则层 -> 执行层 -> 产出层 -> 质控层”的顺序执行。

## 3. EpiClaude 优先级

- 当 EpiClaude skills 与旧本地 skills 重叠时，优先使用 EpiClaude：`biostat-principles`、`r-biostats`、`project-init`、`publication-figures`、`academic-publishing`、`consulting-delivery`、`epi-project-audit`、`humanizer-zh`。
- 统计分析和咨询工作优先 EpiClaude，而不是旧的 `epi-biostat-consulting`。
- 论文配图和科研绘图优先 EpiClaude 的 `publication-figures`，除非用户明确要求 Nature/Science/Elsevier 等特定风格。
- 文档格式工具按文件类型选择：`.docx` 用 `docx`，`.pdf` 用 `pdf`，`.pptx` 用 `pptx`，`.xlsx/.csv/.tsv` 用 `xlsx` 或 Spreadsheets 插件。
- 已弃用 / 仅作后备的本地 skill（其 `SKILL.md` 描述已改为委派，不应再就广义任务自动触发）：`doc`（→ `docx`）、`epi-biostat-consulting`（→ EpiClaude 分析链）、`nature-figure` / `sci-figure` / `paper-figure-style-router`（仅当用户明确点名某期刊视觉样式时使用，常规出图 → `publication-figures`）。`clinical-public-health-research` 仅用于 EpiClaude 链未覆盖的英文研究设计 / 评审环节。

## 3bis. 安装时的冲突自动停用（硬规则）

把本框架 skill 装入使用者 `CODEX_HOME/skills/` 时，安装代理必须执行以下步骤，不等用户点名：

1. 遍历使用者现有 `skills/` 下每个 `SKILL.md` 的 `description`；
2. 比对本框架权威 skill 的触发场景，识别会发生调用冲突的现有 skill——即同一广义触发（如"出图/论文配图""统计分析""写论文"".docx 处理"）会被多个 skill 同时抢占；
3. 直接停用每个冲突 skill：把其 `SKILL.md` 的 `description` 改写为"已停用 / 委派给对应权威 skill"，使其不再就广义任务自动触发（改写描述、保留文件，可逆；需硬停用时再把 `SKILL.md` 改名为 `SKILL.md.disabled`）；
4. 不删除、不覆盖使用者原 skill 的正文内容，只改 `description` 这一路由开关；
5. 登记并汇报：列出被停用的 skill、判定为冲突的触发词、改为委派的目标权威 skill，供使用者复核。

判定以 EpiClaude 权威 skill 为准，使用者侧同域旧 skill 一律降级为后备。

## 4. 研究项目硬规则

- 不修改 `01_data/rawdata/` 原始数据；清洗结果和派生数据另存。
- 研究项目代码尽量使用项目相对路径；不要把个人机器绝对路径写入可复现脚本。
- 不在项目根目录长期放临时脚本、测试输出或零散结果；一次性脚本和旧版文件归入 `09_backup/`。
- `02_code/` 只放可从原始数据复现到最终结果的主流程脚本；脚本编号连续，避免 `test.R`、`final.R`、`temp.R`、`main.R` 等无法审计的命名。
- 表图编号按论文行文顺序连续；主表 `Table{N}_*.xlsx`，附表 `TableS{N}_*`，主图 `Fig{N}_*`，附图 `FigS{N}_*`。
- 表图编号应由 registry 或单一清单控制；不要在多个脚本中手写散落的 `Table6`、`Fig3` 等编号。
- 结果变化同步 `07_paper/0_result_summaries.md`；方法、口径或重要决策变化同步 `DECISIONS.md`；阶段操作同步 `SESSION_LOG.md`。
- 口径常量集中管理，例如有序因子水平、P 值格式、表格组成、配色、字体、输出路径规则。
- 探索性方法或模型优化先进入 `09_backup/<日期>_<主题>/` 隔离实验；只有与主流程公平对照且确有稳健改进，才合并回主流程。

## 5. 运行与自我纠错门禁

- 写完代码后必须真实运行：R 用 `Rscript` 或项目既定入口，Python 用项目环境实际执行；不能只写代码就报告完成。
- 运行后全量扫描日志或输出中的 `error|warning|traceback|failed|nan|NaN`，不能只看最后几行。
- 每个 error/warning 必须归类处理：代码 bug 则修复重跑；数据问题则写明原因和影响范围；库噪声则记录核实证据。
- 表格、图件、Word、PPT、PDF、Excel 交付物生成后要打开、渲染或用脚本检查关键内容，确认不是空文件、乱码、错列、错图或路径失效。
- 完成前进行同类问题扫查：发现一个命名、格式、乱码、口径或编号问题，要 grep/遍历检查同类问题并一次性修复。
- 不跳过失败文件；中文 IO 或文件锁导致失败时，先修复读取/写入流程，再继续完成全量处理。

## 6. 交付与写作规范

- 对外交付物应可独立复现：包含代码、输入说明、环境说明、结果文件、运行顺序和必要解释。
- 论文、报告、PPT、表图和 README 不出现 AI 工作痕迹、AI 助手口吻、emoji、模板式免责声明或“待人工复核/机辅待核”等未完成措辞。
- 中文学术文本默认使用专业书面语；减少空泛连接词，增加具体研究对象、变量、结果和限制条件。
- 英文缩写首次出现给全称；标题优先名词短语，避免反问式标题。
- 不把探索性峰值、网格搜索标签或调参结果包装成临床结论；没有证据时避免“最佳”“证明”“显著优于”等过度表达。

## 7. 推荐目录骨架

```text
01_data/rawdata/   只读原始数据
02_code/           编号脚本 + config/conventions/lib
03_tables/         Table{N}_*.xlsx；附表进 supplementary/
04_figures/        Fig{N}_*.pdf/png；附图进 supplementary/
05_reports/        咨询或外发交付包
06_results/        中间对象，按内容命名
07_paper/          论文文稿 + 0_result_summaries.md
09_backup/         旧版、一次性脚本、探索实验
DECISIONS.md       方法和口径决策
SESSION_LOG.md     阶段操作记录
```

## 8. 完成前检查

- 对应 skill 已加载并执行。
- TODO 状态机已走到 VERIFY/DOCUMENT。
- 代码或文档产物已实际运行、渲染或打开检查。
- 全量 error/warning/NaN/乱码检查已完成。
- 表图编号、文件命名、正文引用和输出路径一致。
- 结果同步 `0_result_summaries.md`，方法同步 `DECISIONS.md`，操作同步 `SESSION_LOG.md`。
- 一次性脚本、旧版本、探索文件已归档。
- 对外文本已去除 AI 助手口吻和未完成措辞。