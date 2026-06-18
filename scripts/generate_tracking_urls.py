"""Generate Kromi Facebook group tracking IDs and URLs.

Input:
    marketing/facebook-groups/Kromi_50_Verified_Groups_with_Data.csv

Output:
    marketing/facebook-groups/Kromi_50_Verified_Groups_TRACKING.csv
"""

from __future__ import annotations

from pathlib import Path
import pandas as pd

BASE_URL = "https://kromiuniverse.com/arc"
INPUT_PATH = Path("marketing/facebook-groups/Kromi_50_Verified_Groups_with_Data.csv")
OUTPUT_PATH = Path("marketing/facebook-groups/Kromi_50_Verified_Groups_TRACKING.csv")

REQUIRED_COLUMNS = [
    "Tracking ID",
    "Tracking URL",
    "Membership Status",
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
]


def main() -> None:
    df = pd.read_csv(INPUT_PATH)

    for column in REQUIRED_COLUMNS:
        if column not in df.columns:
            df[column] = ""

    for index, row in df.iterrows():
        tracking_id = str(row.get("Tracking ID", "")).strip()
        if not tracking_id:
            tracking_id = f"fb_{index + 1:03d}"
            df.at[index, "Tracking ID"] = tracking_id

        tracking_url = str(row.get("Tracking URL", "")).strip()
        if not tracking_url:
            df.at[index, "Tracking URL"] = f"{BASE_URL}?group={tracking_id}"

        if not str(row.get("Status", "")).strip():
            df.at[index, "Status"] = "Not contacted"

        if not str(row.get("Membership Status", "")).strip():
            df.at[index, "Membership Status"] = "Not member"

        if not str(row.get("Post Result", "")).strip():
            df.at[index, "Post Result"] = "Not attempted"

        if not str(row.get("Post Attempt Count", "")).strip():
            df.at[index, "Post Attempt Count"] = 0

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_PATH, index=False)
    print(f"Saved: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
