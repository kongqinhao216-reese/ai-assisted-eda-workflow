# AI-Assisted EDA Workflow 求职项目报告

## 项目名称

AI-Assisted EDA Workflow / AI 辅助探索性数据分析工作流

## 项目简介

该项目构建了一个面向数据分析场景的半自动 EDA 工作流，目标是提升原始数据探索、质量检查、问题识别、清洗决策和分析记录的系统性。

项目以 Jupyter Notebook 为主流程入口，结合独立 Python 辅助模块，实现从数据加载、数据质量检测、问题日志生成、交互式处理决策，到 AI 评估摘要和后续预处理的完整闭环。

项目强调“决策驱动的数据清洗”，避免直接对原始数据进行盲目修改。原始数据保留为 `df`，清洗后的数据保存在 `df_clean`，并通过 `issue_log` 和 `cleaning_log` 记录数据问题、处理方案和验证结果，使整个分析过程更可追踪、可复核、可解释。

## 核心功能

- 设计并实现 AI 辅助 EDA Notebook 模板，覆盖数据读取、预览、类型检查、缺失值检查、重复值检查、唯一值分析和范围分布检查。
- 开发 `eda_review_assistant.py` 辅助模块，自动生成结构化 `issue_log`，识别缺失值、高唯一值字段、常量列、疑似日期字段、负值异常和重复行等问题。
- 构建交互式处理决策流程，支持用户针对每个数据问题选择处理方案或输入自定义处理说明。
- 增加 AI Assessment Summary 流程，用于在执行清洗前评估处理方案的合理性、风险和业务确认项。
- 将数据预处理流程改造为 `df_clean` 驱动，确保原始数据不被直接覆盖。
- 编写中英文项目文档，并将项目上传至 GitHub，便于展示和复用。

## 技术栈

Python, Pandas, NumPy, Matplotlib, Seaborn, Skimpy, ipywidgets, Jupyter Notebook, Git, GitHub

## 项目亮点

- 将传统 EDA 模板升级为“问题识别 + 决策记录 + AI 评估 + 清洗验证”的半自动分析流程。
- 使用 `issue_log` 作为数据质量问题的统一管理表，使数据清洗不再依赖零散 Notebook 代码。
- 通过 `df` / `df_clean` 分离原始数据和清洗数据，提高数据处理安全性。
- 引入 `cleaning_log` 思路，记录每一步清洗动作的原因和验证方式，增强分析过程的可解释性。
- 支持中英文 README，具备良好的项目展示和协作基础。

## 简历版项目描述

AI-Assisted EDA Workflow：基于 Python 和 Jupyter Notebook 构建半自动探索性数据分析工作流，覆盖数据质量检查、问题日志生成、交互式处理决策、AI 评估摘要和清洗验证。开发独立辅助模块自动识别缺失值、重复行、高唯一值字段、常量列、疑似日期字段和异常负值，并通过 `issue_log` / `cleaning_log` 提升数据清洗过程的可追踪性和可解释性。项目已整理中英文文档并发布至 GitHub。

## 英文简历 Bullet Points

- Built an AI-assisted EDA workflow with Python, Pandas, and Jupyter Notebook to standardize data inspection, issue detection, preprocessing decisions, and validation.
- Developed a reusable helper module to generate structured `issue_log` records for missing values, duplicates, high-cardinality columns, constant columns, possible datetime fields, and suspicious numeric values.
- Designed a decision-driven preprocessing process using `df_clean` and `cleaning_log` to preserve raw data and document every approved transformation.
- Added bilingual documentation and published the project to GitHub for portfolio presentation and reuse.

## 面试表达版

这个项目来源于我对传统 EDA Notebook 的改造。普通 EDA 模板通常只是给出一系列检查代码，但缺少“发现问题后如何决策”的流程。因此我设计了一个 AI 辅助的 EDA 工作流：先系统检查数据质量，再自动生成问题日志 `issue_log`，然后通过交互方式记录处理决策，最后让 AI 对这些决策进行评估，再进入数据清洗阶段。

我特别强调不直接修改原始数据，而是保留 `df`，在 `df_clean` 上执行清洗，并通过 `cleaning_log` 记录每一步操作的原因和验证方式。这个项目体现了我对数据分析流程、数据质量控制和可解释性分析的理解。
