---
name: epiclaude-priority
description: Use for epidemiology, biostatistics, public-health research, R or Python statistical analysis, manuscript writing, publication figures, consulting delivery, project audit, Chinese academic polishing, or when user mentions EpiClaude, 流行病学, 卫生统计, 生统, 论文, 投稿, 咨询交付, 去AI味, 发表级图表. When this overlaps with existing local skills, EpiClaude skills are authoritative.
---

# EpiClaude Priority

This skill sets source priority for the EpiClaude skill ecosystem installed from `KangWang42/EpiClaude`.

## Priority Rule

When EpiClaude overlaps with older local skills, use EpiClaude as the authoritative workflow.

Use this mapping:
- General epidemiology/biostatistics guardrails: `biostat-principles`
- R statistical analysis, regression, survival, mediation, meta-analysis, visualization: `r-biostats`
- New project structure and reproducibility scaffolding: `project-init`
- Publication figures and scientific palettes: `publication-figures`
- Manuscript writing, submission materials, reviewer response: `academic-publishing`
- Chinese academic style and anti-AI polishing: `humanizer-zh`
- Consulting deliverables and reproducible handoff packages: `consulting-delivery`
- Project/result/code/manuscript audit: `epi-project-audit`
- SYSU/medical group-meeting slides: `sysu-ppt`

## Conflict Handling

- Prefer EpiClaude over `epi-biostat-consulting` for statistical analysis workflows.
- Prefer EpiClaude over `clinical-public-health-research` when the task is workflow, project structure, analysis, writing, or delivery.
- Prefer EpiClaude `publication-figures` over `nature-figure`, `sci-figure`, and `paper-figure-style-router` unless the user explicitly asks for those styles.
- Prefer EpiClaude `pdf`, `docx`, `pptx`, and `xlsx` for document tooling when their names match the requested file type.

## Execution Standard

Follow EpiClaude's gate style: plan, code, run, verify, document. Do not mark analysis or delivery tasks complete until outputs are actually generated or the blocker is explicitly documented.

For full cross-task global rules, read [references/CLAUDE.md](references/CLAUDE.md) on demand.
