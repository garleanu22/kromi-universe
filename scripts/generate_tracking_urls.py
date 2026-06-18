"""Prepare the Kromi Facebook Groups CRM for tracking.

Input:
    marketing/facebook-groups/Kromi_50_Verified_Groups_with_Data.csv

Output:
    marketing/facebook-groups/Kromi_50_Verified_Groups_TRACKING.csv
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd

BASE_URL = "https://kromiuniverse.com/arc"
INPUT_PATH = Path("marketing/facebook-groups/Kromi_50_Verified_Groups_with_Data.csv")
OUTPUT_PATH = Path("marketing/facebook-groups/Kromi_50_Verified_Groups_TRACKING.csv")

REQUIRED_COLUMNS = [
    "Group Name",
    "Facebook URL",
    "Segment",
    "Priority",
    "Parents 4-8 Score",
    "Book Promotion Allowed",
    "Engagement",
    "Group Size",
    "English Audience",
    "ARC Friendly",
    "Review Potential",
    "Kromi Fit",
    "Status",
    "Membership Status",
    "Tracking ID",
    "Tracking URL",
    "Join Requested Date",
    "Check Again Date",
    "Post Result",
    "Post Date",
    "Post URL",
    "Post Attempt Count",
    "GA4 Visitors",
    "ARC Signups",
    "Amazon Clicks",
    "Reviews Generated",
    "Visitor to ARC Signup Rate",
    "ARC to Review Rate",
    "Outcome Score",
    "Last Checked",
    "Last Error",
    "Notes",
]

PRIORITY_RANK = {
    "A+": 0,
    "A": 1,
    "B": 2,
    "C": 3,
}


def clean_text(value: Any) -> str:
    if pd.isna(value):
        return ""
    return str(value).strip()


def is_blank(value: Any) -> bool:
    return clean_text(value) == ""


def score_numeric(value: Any) -> float:
    number = pd.to_numeric(value, errors="coerce")
    if pd.isna(number):
        return 0
    return float(number)


def validate_source_columns(df: pd.DataFrame) -> list[str]:
    issues = []
    required_source_columns = [
        "Group Name",
        "Facebook URL",
        "Priority",
        "Review Potential",
        "Kromi Fit",
        "ARC Friendly",
        "Status",
    ]
    for column in required_source_columns:
        if column not in df.columns:
            issues.append(f"Missing source column added as blank: {column}")

    if "Facebook URL" in df.columns:
        blank_urls = df["Facebook URL"].apply(is_blank).sum()
        if blank_urls:
            issues.append(f"Rows with blank Facebook URL: {blank_urls}")

    if "Group Name" in df.columns:
        blank_names = df["Group Name"].apply(is_blank).sum()
        if blank_names:
            issues.append(f"Rows with blank Group Name: {blank_names}")

    return issues


def add_missing_columns(df: pd.DataFrame) -> list[str]:
    added = []
    for column in REQUIRED_COLUMNS:
        if column not in df.columns:
            df[column] = ""
            added.append(column)
    return added


def prepare_tracking(df: pd.DataFrame) -> tuple[int, int]:
    tracking_ids_created = 0
    tracking_urls_created = 0

    for index, row in df.iterrows():
        tracking_id = clean_text(row.get("Tracking ID", ""))
        if not tracking_id:
            tracking_id = f"fb_{index + 1:03d}"
            df.at[index, "Tracking ID"] = tracking_id
            tracking_ids_created += 1

        tracking_url = clean_text(row.get("Tracking URL", ""))
        if not tracking_url:
            df.at[index, "Tracking URL"] = f"{BASE_URL}?group={tracking_id}"
            tracking_urls_created += 1

        if is_blank(row.get("Status", "")):
            df.at[index, "Status"] = "Not contacted"

        if is_blank(row.get("Membership Status", "")):
            df.at[index, "Membership Status"] = "Not member"

        if is_blank(row.get("Post Result", "")):
            df.at[index, "Post Result"] = "Not attempted"

        if is_blank(row.get("Post Attempt Count", "")):
            df.at[index, "Post Attempt Count"] = "0"

    return tracking_ids_created, tracking_urls_created


def sorted_next_groups(df: pd.DataFrame) -> pd.DataFrame:
    ranked = df.copy()
    ranked["_priority_rank"] = ranked["Priority"].map(PRIORITY_RANK).fillna(99)
    ranked["_review_potential"] = ranked["Review Potential"].apply(score_numeric)
    ranked["_kromi_fit"] = ranked["Kromi Fit"].apply(score_numeric)
    ranked["_arc_friendly_rank"] = ranked["ARC Friendly"].apply(
        lambda value: 0 if clean_text(value).lower() == "yes" else 1
    )
    ranked["_status_rank"] = ranked["Status"].apply(
        lambda value: 0 if clean_text(value) == "Not contacted" else 1
    )

    return ranked.sort_values(
        by=[
            "_priority_rank",
            "_review_potential",
            "_kromi_fit",
            "_arc_friendly_rank",
            "_status_rank",
        ],
        ascending=[True, False, False, True, True],
        kind="mergesort",
    ).drop(
        columns=[
            "_priority_rank",
            "_review_potential",
            "_kromi_fit",
            "_arc_friendly_rank",
            "_status_rank",
        ]
    )


def print_report(
    *,
    rows_processed: int,
    columns_added: list[str],
    tracking_ids_created: int,
    tracking_urls_created: int,
    next_groups: pd.DataFrame,
    issues: list[str],
) -> None:
    print(f"Saved: {OUTPUT_PATH}")
    print(f"Rows processed: {rows_processed}")
    print(f"Tracking IDs created: {tracking_ids_created}")
    print(f"Tracking URLs created: {tracking_urls_created}")
    print(f"Missing columns added: {len(columns_added)}")
    for column in columns_added:
        print(f"- {column}")

    print("Next 5 priority groups:")
    for _, row in next_groups.head(5).iterrows():
        print(
            "- "
            f"{clean_text(row['Group Name'])} "
            f"({clean_text(row['Priority'])}, "
            f"Review Potential {clean_text(row['Review Potential'])}, "
            f"Kromi Fit {clean_text(row['Kromi Fit'])}, "
            f"ARC Friendly {clean_text(row['ARC Friendly'])}, "
            f"Status {clean_text(row['Status'])})"
        )

    print("Issues found:")
    if issues:
        for issue in issues:
            print(f"- {issue}")
    else:
        print("- None")


def main() -> None:
    df = pd.read_csv(INPUT_PATH)
    issues = validate_source_columns(df)
    columns_added = add_missing_columns(df)
    tracking_ids_created, tracking_urls_created = prepare_tracking(df)
    next_groups = sorted_next_groups(df)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_PATH, index=False)
    print_report(
        rows_processed=len(df),
        columns_added=columns_added,
        tracking_ids_created=tracking_ids_created,
        tracking_urls_created=tracking_urls_created,
        next_groups=next_groups,
        issues=issues,
    )


if __name__ == "__main__":
    main()
