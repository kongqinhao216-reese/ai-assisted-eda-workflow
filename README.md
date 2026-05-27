# AI-Assisted EDA Workflow

This project provides a semi-automated workflow template for exploratory data analysis (EDA). After a raw dataset is added, the notebook guides the user through data loading, quality checks, issue detection, treatment decisions, AI assessment, preprocessing, and basic analysis.

The goal is not to let AI blindly modify the data. Instead, the workflow helps AI support a controlled and reviewable process: detect issues, record them, decide how to handle them, evaluate the decisions, and only then apply preprocessing.

For the Chinese version, see [README.zh-CN.md](README.zh-CN.md).

## Project Files

- `eda_automation.ipynb`: Main notebook for data loading, checks, review, preprocessing, and analysis.
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
