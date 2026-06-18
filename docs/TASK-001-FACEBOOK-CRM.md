# TASK-001 — Facebook Groups CRM Automation

## Goal

Prepare the Kromi Facebook Groups CRM for automated tracking and daily reporting.

Do not automate Facebook posting yet.

## Source file

Use:

marketing/facebook-groups/Kromi_50_Verified_Groups_with_Data.csv

## Required columns

Validate the CRM file and create missing columns:

- Group Name
- Facebook URL
- Segment
- Priority
- Parents 4-8 Score
- Book Promotion Allowed
- Engagement
- Group Size
- English Audience
- ARC Friendly
- Review Potential
- Kromi Fit
- Status
- Membership Status
- Tracking ID
- Tracking URL
- Join Requested Date
- Check Again Date
- Post Result
- Post Date
- Post URL
- Post Attempt Count
- GA4 Visitors
- ARC Signups
- Amazon Clicks
- Reviews Generated
- Visitor to ARC Signup Rate
- ARC to Review Rate
- Outcome Score
- Last Checked
- Last Error
- Notes

Do not overwrite existing data.

## Tracking IDs

Generate sequential IDs:

fb_001
fb_002
fb_003

## Tracking URLs

Generate:

https://kromiuniverse.com/arc?group=fb_001

Use the Tracking ID from each row.

## Sorting logic for daily outreach

When selecting next groups, sort by:

1. Priority: A+ > A > B > C
2. Review Potential descending
3. Kromi Fit descending
4. ARC Friendly = Yes first
5. Status = Not contacted first

## Status values

Use these values:

- Not contacted
- Join requested
- Pending approval
- Joined
- Ready to post
- Posted
- Skipped
- Failed

## Post Result values

Use these values:

- Not attempted
- Success
- Failed
- Awaiting moderation
- Removed
- Not allowed
- Unknown

## Output

Save the processed CRM as:

marketing/facebook-groups/Kromi_50_Verified_Groups_TRACKING.csv

Return a short report with:

- rows processed
- tracking IDs created
- tracking URLs created
- missing columns added
- next 5 priority groups
- issues found
