"""Utilities for reviewing EDA findings before preprocessing.

The module is intentionally lightweight so it can be imported from a notebook
without turning the notebook into a large application.
"""

from __future__ import annotations

import warnings
from typing import Dict, List, Optional

import pandas as pd


DecisionOptions = Dict[str, List[str]]


DEFAULT_DECISION_OPTIONS: DecisionOptions = {
    "missing_values": [
        "keep_missing",
        "drop_rows",
        "impute_median",
        "impute_mode",
        "add_missing_flag",
        "custom",
    ],
    "constant_column": ["drop_column", "keep_column", "custom"],
    "high_cardinality": [
        "mark_as_identifier",
        "keep_for_reference",
        "drop_from_analysis",
        "custom",
    ],
    "possible_datetime": ["convert_to_datetime", "keep_as_text", "custom"],
    "negative_values": [
        "validate_with_business_rule",
        "filter_invalid_rows",
        "cap_or_winsorize",
        "custom",
    ],
    "duplicate_rows": ["drop_exact_duplicates", "keep_duplicates", "custom"],
}


def _safe_nunique(series: pd.Series, dropna: bool = False) -> int:
    """Count unique values, falling back for columns with list/dict objects."""

    try:
        return int(series.nunique(dropna=dropna))
    except TypeError:
        return int(series.astype(str).nunique(dropna=dropna))


def build_issue_log(df: pd.DataFrame, datetime_sample_size: int = 100) -> pd.DataFrame:
    """Build a review table of likely data-quality issues.

    The result is a decision log, not an instruction to modify data. Each row
    should be reviewed before preprocessing code is applied.
    """

    issue_records = []
    row_count = len(df)

    for col in df.columns:
        series = df[col]
        missing_count = int(series.isna().sum())
        missing_pct = (missing_count / row_count * 100) if row_count else 0
        unique_count = _safe_nunique(series, dropna=False)
        unique_pct = (unique_count / row_count * 100) if row_count else 0

        if missing_count > 0:
            issue_records.append(
                {
                    "column": col,
                    "issue_type": "missing_values",
                    "finding": f"{missing_count} missing values ({missing_pct:.2f}%).",
                    "suggested_action": (
                        "Investigate missingness, then keep, impute, drop, or flag."
                    ),
                    "status": "pending",
                    "decision": "",
                }
            )

        if unique_count == 1:
            issue_records.append(
                {
                    "column": col,
                    "issue_type": "constant_column",
                    "finding": "Only one unique value was found.",
                    "suggested_action": (
                        "Review whether the column carries analytical value."
                    ),
                    "status": "pending",
                    "decision": "",
                }
            )
        elif unique_pct > 90:
            issue_records.append(
                {
                    "column": col,
                    "issue_type": "high_cardinality",
                    "finding": f"{unique_count} unique values ({unique_pct:.2f}%).",
                    "suggested_action": (
                        "Confirm whether this is an identifier, timestamp, or free-text field."
                    ),
                    "status": "pending",
                    "decision": "",
                }
            )

        if pd.api.types.is_object_dtype(series):
            sample = series.dropna().astype(str).head(datetime_sample_size)
            if len(sample):
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore", UserWarning)
                    parsed = pd.to_datetime(sample, errors="coerce")
                if parsed.notna().mean() >= 0.8:
                    issue_records.append(
                        {
                            "column": col,
                            "issue_type": "possible_datetime",
                            "finding": (
                                "Object column appears to contain date-like values."
                            ),
                            "suggested_action": (
                                "Consider converting to datetime with pd.to_datetime."
                            ),
                            "status": "pending",
                            "decision": "",
                        }
                    )

        if pd.api.types.is_numeric_dtype(series):
            min_value = series.min(skipna=True)
            if pd.notna(min_value) and min_value < 0:
                issue_records.append(
                    {
                        "column": col,
                        "issue_type": "negative_values",
                        "finding": f"Minimum value is {min_value}.",
                        "suggested_action": (
                            "Validate whether negative values are allowed by business rules."
                        ),
                        "status": "pending",
                        "decision": "",
                    }
                )

    try:
        duplicate_count = int(df.duplicated().sum())
    except TypeError:
        duplicate_count = int(df.astype(str).duplicated().sum())
    if duplicate_count > 0:
        issue_records.append(
            {
                "column": "<entire row>",
                "issue_type": "duplicate_rows",
                "finding": f"{duplicate_count} entirely duplicated rows were found.",
                "suggested_action": (
                    "Confirm whether duplicates are import errors or legitimate repeated events."
                ),
                "status": "pending",
                "decision": "",
            }
        )

    return pd.DataFrame(
        issue_records,
        columns=[
            "column",
            "issue_type",
            "finding",
            "suggested_action",
            "status",
            "decision",
        ],
    )


def build_ai_assessment_prompt(
    issue_log: pd.DataFrame,
    dataset_context: str = "",
    field_definitions: str = "",
) -> str:
    """Create a structured prompt for AI review of preprocessing decisions."""

    if issue_log.empty:
        issue_markdown = "No obvious issues were detected."
    else:
        issue_markdown = issue_log.to_string(index=False)

    return f"""Review the EDA issue log and evaluate the proposed preprocessing decisions.

Dataset context:
{dataset_context or "[Add business background, project goal, and unit of analysis.]"}

Field definitions:
{field_definitions or "[Add column meanings, valid ranges, and business rules.]"}

Issue log:
{issue_markdown}

Please produce:
1. Assessment of whether each decision is reasonable.
2. Risks or assumptions for each preprocessing action.
3. Items that require business confirmation.
4. Approved preprocessing plan with validation checks.
"""


def summarize_decisions(issue_log: pd.DataFrame) -> str:
    """Return a compact markdown handoff for the preprocessing section."""

    if issue_log.empty:
        return "No preprocessing issues were recorded by the EDA Review Assistant."

    decided = issue_log[issue_log["status"].eq("decided")].copy()
    pending = issue_log[~issue_log["status"].eq("decided")].copy()
    lines = ["### AI Assessment Summary", ""]

    if not decided.empty:
        lines.append("**Approved / Selected Decisions**")
        for _, row in decided.iterrows():
            lines.append(
                f"- `{row['column']}` ({row['issue_type']}): {row['decision']}"
            )
        lines.append("")

    if not pending.empty:
        lines.append("**Items Requiring Review**")
        for _, row in pending.iterrows():
            lines.append(
                f"- `{row['column']}` ({row['issue_type']}): {row['finding']}"
            )
        lines.append("")

    lines.append("**Preprocessing Rule**")
    lines.append("- Apply only reviewed decisions, and validate every transformation.")
    return "\n".join(lines)


def render_decision_widget(
    issue_log: pd.DataFrame,
    decision_options: Optional[DecisionOptions] = None,
):
    """Render an ipywidgets decision helper and mutate issue_log in place."""

    if issue_log.empty:
        print("There are no pending issues to review.")
        return None

    try:
        import ipywidgets as widgets
        from IPython.display import display
    except ImportError:
        print("ipywidgets is not installed. Install requirements, then rerun this cell.")
        return None

    options = decision_options or DEFAULT_DECISION_OPTIONS

    issue_selector = widgets.Dropdown(
        options=[
            (f"{i}: {row['column']} - {row['issue_type']}", i)
            for i, row in issue_log.iterrows()
        ],
        description="Issue:",
    )
    action_selector = widgets.Dropdown(description="Action:")
    custom_instruction = widgets.Textarea(
        description="Custom:",
        placeholder="Write a custom cleaning instruction here.",
    )
    save_button = widgets.Button(description="Save decision", button_style="primary")
    output = widgets.Output()

    def refresh_actions(change=None):
        issue_type = issue_log.loc[issue_selector.value, "issue_type"]
        action_selector.options = options.get(issue_type, ["custom"])

    def save_decision(_):
        selected = issue_selector.value
        action = action_selector.value
        decision = custom_instruction.value.strip() if action == "custom" else action
        issue_log.loc[selected, "decision"] = decision
        issue_log.loc[selected, "status"] = "decided"
        with output:
            output.clear_output()
            display(issue_log)

    issue_selector.observe(refresh_actions, names="value")
    save_button.on_click(save_decision)
    refresh_actions()
    return widgets.VBox(
        [issue_selector, action_selector, custom_instruction, save_button, output]
    )
