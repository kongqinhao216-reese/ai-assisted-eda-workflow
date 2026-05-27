# AI-Assisted EDA Workflow

## 中文说明

这是一个用于探索性数据分析（EDA）的半自动工作流模板。假设你已经加入了一个原始数据集，本项目会引导你从数据读取、质量检查、问题识别、处理决策、AI 评估，到最终进入清洗和分析。

这个项目的重点不是让 AI 直接修改数据，而是让 AI 辅助你更有条理地完成 EDA：先发现问题，再记录问题，再决定处理方式，最后才执行清洗。

## 项目文件

- `eda_automation.ipynb`：主要 Notebook，按流程完成数据加载、检查、决策、预处理和基础分析。
- `eda_review_assistant.py`：辅助模块，用于生成 `issue_log`、展示交互式处理选项、生成 AI 评估提示。
- `requirements.txt`：项目依赖版本范围。

## 推荐工作流

1. 将数据集放入项目目录，或在 Notebook 中填写正确的数据路径。
2. 运行依赖安装单元格，确保环境具备所需库。
3. 在 Notebook 中加载数据，并将原始数据保存为 `df`。
4. 执行基础数据检查，包括行列数、样本预览、类型、缺失值、重复值、唯一值和范围分布。
5. 使用 EDA Review Assistant 生成 `issue_log`。
6. 针对每个数据问题选择处理方案，或输入自定义处理说明。
7. 生成 AI Assessment Summary，用于评估处理方案是否合理。
8. 在 Data Preprocessing 部分创建 `df_clean`，只执行已经确认的处理。
9. 使用验证代码和 `cleaning_log` 记录清洗结果。
10. 基于 `df_clean` 进行基础分析，并从基础结论引导更深层问题。

## 使用原则

- 不直接修改原始 `df`，清洗应在 `df_clean` 中完成。
- 不因为模板里有某个步骤就执行它，只处理已发现并确认的问题。
- 每个清洗动作都应有原因、代码和验证。
- AI 的作用是辅助判断和生成建议，最终处理方案应结合数据含义和业务背景确认。

## English

This is a semi-automated workflow template for exploratory data analysis (EDA). Assuming a raw dataset has been added, the project guides you through data loading, quality checks, issue detection, treatment decisions, AI assessment, preprocessing, and basic analysis.

The goal is not to let AI blindly modify the data. Instead, the workflow helps you use AI in a controlled way: detect issues, record them, decide how to handle them, evaluate the decisions, and only then apply preprocessing.

## Project Files

- `eda_automation.ipynb`: The main notebook for data loading, checks, review, preprocessing, and analysis.
- `eda_review_assistant.py`: Helper module for building `issue_log`, rendering decision options, and generating AI assessment prompts.
- `requirements.txt`: Dependency version ranges for the project.

## Recommended Workflow

1. Place the dataset in the project folder, or set the correct data path in the notebook.
2. Run the dependency setup cell if needed.
3. Load the raw dataset into a DataFrame named `df`.
4. Run basic data checks: shape, previews, data types, missing values, duplicates, uniqueness, and value ranges.
5. Use the EDA Review Assistant to generate `issue_log`.
6. Select a treatment option for each issue, or write a custom instruction.
7. Generate an AI Assessment Summary to evaluate whether the proposed decisions are reasonable.
8. In the Data Preprocessing section, create `df_clean` and apply only approved decisions.
9. Validate the transformations and document them in `cleaning_log`.
10. Analyze `df_clean`, starting with conservative findings and then moving toward deeper questions.

## Guiding Principles

- Do not modify the original `df`; apply cleaning steps to `df_clean`.
- Do not run a preprocessing step just because it exists in the template.
- Every cleaning action should include a reason, implementation, and validation.
- AI should support decision-making, but final preprocessing choices should be grounded in data meaning and business context.
