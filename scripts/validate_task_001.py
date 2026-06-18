"""Validate TASK-001 Facebook CRM tracking output."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

SOURCE_PATH = Path("marketing/facebook-groups/Kromi_50_Verified_Groups_with_Data.csv")
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


def main() -> None:
    source = pd.read_csv(SOURCE_PATH)
    output = pd.read_csv(OUTPUT_PATH, dtype=str).fillna("")

    issues = []
    if len(source) != len(output):
        issues.append(f"Row count mismatch: source={len(source)} output={len(output)}")

    missing_columns = [column for column in REQUIRED_COLUMNS if column not in output.columns]
    if missing_columns:
        issues.append(f"Missing required output columns: {missing_columns}")

    expected_ids = [f"fb_{index + 1:03d}" for index in range(len(output))]
    actual_ids = output["Tracking ID"].tolist()
    if actual_ids != expected_ids:
        issues.append("Tracking IDs are not sequential from fb_001")

    expected_urls = [f"https://kromiuniverse.com/arc?group={tracking_id}" for tracking_id in expected_ids]
    actual_urls = output["Tracking URL"].tolist()
    if actual_urls != expected_urls:
        issues.append("Tracking URLs do not match Tracking IDs")

    source_columns = list(source.columns)
    comparable = output[source_columns].astype(str).fillna("")
    original = source.astype(str).fillna("")
    if not comparable.equals(original):
        issues.append("Source column values changed in output")

    print(f"Rows processed: {len(output)}")
    print(f"Required columns present: {not missing_columns}")
    print(f"Sequential tracking IDs: {actual_ids == expected_ids}")
    print(f"Tracking URLs match IDs: {actual_urls == expected_urls}")
    print(f"Source columns preserved: {comparable.equals(original)}")
    print("Validation issues:")
    if issues:
        for issue in issues:
            print(f"- {issue}")
        raise SystemExit(1)
    print("- None")


if __name__ == "__main__":
    main()
