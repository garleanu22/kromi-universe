# TASK-002 - ARC Landing Page Tracking

## Goal

Prepare the Kromi ARC landing page to capture Facebook group tracking IDs from URLs such as:

```text
https://kromiuniverse.com/arc?group=fb_001
```

This task prepares documentation and reusable client-side code only. It does not modify the live website, automate Facebook posting, implement GA4 API reporting, or implement Kit API reporting.

## Source Of Truth

Facebook group attribution starts in:

```text
marketing/facebook-groups/Kromi_50_Verified_Groups_TRACKING.csv
```

Relevant CRM columns:

- `Tracking ID`
- `Tracking URL`
- `GA4 Visitors`
- `ARC Signups`
- `Amazon Clicks`
- `Reviews Generated`
- `Outcome Score`

The landing page must preserve the `Tracking ID` value from the `group` URL parameter so later reporting can map events and signups back to the CRM row.

## Capture Requirement

When a visitor lands on the ARC page with this URL:

```text
/arc?group=fb_001
```

The site should:

1. Read the URL parameter named `group`.
2. Validate that the value looks like a Facebook CRM tracking ID.
3. Store the value for the current browser session.
4. Populate the ARC signup form hidden field.
5. Send GA4 events with `source_group`.
6. Allow Kit to receive the same value in a custom field named `source_group`.

Recommended tracking ID validation:

```text
fb_001
fb_002
fb_050
```

Use this pattern for TASK-002:

```text
^fb_[0-9]{3}$
```

## Storage Requirement

Store the captured value in two places:

1. `sessionStorage`
2. Fallback cookie

Primary browser storage:

```text
sessionStorage key: kromi_source_group
value example: fb_001
```

Fallback cookie:

```text
cookie name: kromi_source_group
value example: fb_001
path: /
max-age: 30 days
SameSite=Lax
Secure when the page is served over HTTPS
```

Use `sessionStorage` as the canonical runtime source. Use the cookie only when `sessionStorage` is unavailable or empty.

## Hidden Form Field Requirement

The ARC signup form should include a hidden field for:

```text
source_group
```

The JavaScript snippet should populate any matching hidden/input field selectors:

```text
input[name="source_group"]
input[name="fields[source_group]"]
input[id="source_group"]
input[data-kromi-source-group]
```

Expected value:

```text
fb_001
```

## Kit Custom Field Requirement

Create or confirm a Kit custom field named:

```text
source_group
```

The embedded Kit form must submit the captured group value into that field.

Depending on the Kit embed markup, the hidden input may need one of these names:

```text
source_group
fields[source_group]
```

The final selector must be verified against the live Kit embed before publishing.

## GA4 Event Requirement

The site should send GA4 events only when `window.gtag` is available. Do not implement GA4 API reporting in TASK-002.

Recommended event names and parameters:

### ARC Landing Visit

```js
gtag("event", "arc_landing_visit", {
  source_group: "fb_001",
  page_location: window.location.href,
  page_path: window.location.pathname
});
```

### ARC Signup Submit

```js
gtag("event", "arc_signup_submit", {
  source_group: "fb_001",
  form_id: "<form id or fallback value>"
});
```

### Amazon Click

```js
gtag("event", "amazon_click", {
  source_group: "fb_001",
  outbound_url: "<clicked Amazon URL>"
});
```

GA4 custom dimensions should later include:

```text
source_group
```

## Implementation Files

Prepared files:

```text
website/custom-js/arc-group-tracking.js
website/snippets/arc-tracking-implementation.md
```

## Test Plan

1. Visit:

```text
https://kromiuniverse.com/arc?group=fb_001
```

2. Verify storage:

```js
sessionStorage.getItem("kromi_source_group")
```

Expected:

```text
fb_001
```

3. Verify fallback cookie:

```js
document.cookie.includes("kromi_source_group=fb_001")
```

Expected:

```text
true
```

4. Verify hidden form field:

```js
document.querySelector('input[name="source_group"], input[name="fields[source_group]"]')?.value
```

Expected:

```text
fb_001
```

5. Verify Kit field:

- Submit a test signup with a controlled email address.
- Confirm the subscriber profile in Kit contains:

```text
source_group = fb_001
```

6. Verify GA4 payload:

- Use GA4 DebugView or Tag Assistant.
- Confirm `arc_landing_visit` includes:

```text
source_group = fb_001
```

- Submit the form and confirm `arc_signup_submit` includes:

```text
source_group = fb_001
```

- Click an Amazon link and confirm `amazon_click` includes:

```text
source_group = fb_001
```

## Access Still Needed

- WordPress admin access or Elementor edit access for the ARC page.
- Confirmation of the exact ARC page URL and whether it is `/arc`.
- Access to the Kit form embed or form editor.
- Confirmation that the Kit custom field `source_group` exists.
- GA4 access with DebugView or Tag Assistant visibility.
- A safe test email address for validating Kit signup attribution.
