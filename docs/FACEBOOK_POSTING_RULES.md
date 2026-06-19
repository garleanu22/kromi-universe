# Facebook Posting Rules

These rules apply to all Kromi Facebook group outreach.

## Source of Truth

Use the CRM file:
marketing/facebook-groups/Kromi_50_Verified_Groups_TRACKING.csv

Never use Facebook group links or tracking links from prompts if the CRM has them.

## Group Selection

Post only in groups where:

- Status is `Not contacted` or `Ready to post`
- Membership Status is `Approved`, `Joined`, or not required
- Posting is allowed by the group rules

Do not post if:

- Status is `Posted`
- Status is `Skipped`
- Status is `Failed` without manual review
- Membership Status is `Pending`
- Group rules forbid book promotion, freebie links, or author promotion

## Post Format

Main post:
- Attach the approved image.
- Do not include the landing page URL.
- Mention that the free copy link is in the first comment.

First comment:
- Use the unique Tracking URL from the selected CRM row.
- Never use the generic landing page URL when posting in tracked groups.

Correct:
https://kromiuniverse.com/landing-page-kromi-1/?group=fb_001

Incorrect:
https://kromiuniverse.com/landing-page-kromi-1/

## Image Asset

Preferred image path:
assets/social/facebook/kromi-free-copy-post.png

If the image is not present in the repo, stop and ask for the asset before posting.

## CRM Updates

After each action, update:

- Status
- Membership Status
- Post Result
- Post Date
- Post URL, if available
- Post Attempt Count
- Last Checked
- Last Error
- Notes

## Post Result Values

Use:

- Not attempted
- Success
- Awaiting moderation
- Failed
- Removed
- Not allowed
- Unknown

## Status Values

Use:

- Not contacted
- Join requested
- Pending approval
- Joined
- Ready to post
- Posted
- Skipped
- Failed

## Safety Rules

- Do not spam.
- Do not post the same text repeatedly in the same group.
- Do not bypass group rules.
- Do not message members directly unless the user explicitly requests it.
- Do not automate high-volume posting.
- Limit posting to the daily number requested by the user.
