# TASK 001 — Kromi Tracking Foundation

## Goal

Create the first functional version of the Facebook Groups tracking system.

Do not automate Facebook posting yet.

## Inputs

Main CRM source:

```text
marketing/facebook-groups/Kromi_50_Verified_Groups_with_Data.csv
```

Main script:

```text
scripts/generate_tracking_urls.py
```

Website JS tracking helper:

```text
website/custom-js/arc-source-tracking.js
```

## Requirements

1. Run the tracking URL generator.
2. Confirm that every group row receives:
   - Tracking ID
   - Tracking URL
   - Status
   - Membership Status
   - Post Result
3. Confirm the URL format:

```text
https://kromiuniverse.com/arc?group=fb_001
```

4. Review `arc-source-tracking.js` and confirm it:
   - reads the `group` parameter
   - stores it in localStorage and cookie
   - populates hidden form fields
   - tracks Amazon clicks through GA4 if `gtag` is available

## Output

Create a short report:

```text
marketing/reports/setup_report_tracking_foundation.md
```

Include:
- number of groups processed
- number of tracking URLs generated
- any missing fields
- next implementation steps

## Do Not

- Do not post to Facebook.
- Do not create separate landing pages.
- Do not track reach or impressions.
- Do not overwrite existing CRM data unless the cell is blank.
