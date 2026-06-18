# ARC Tracking Implementation Notes

## Scope

These notes prepare the WordPress/Elementor implementation for ARC landing page attribution. Do not deploy this until the live ARC page, Kit form, and GA4 DebugView are available for testing.

This implementation does not automate Facebook posting, does not call the GA4 API, and does not call the Kit API.

## Required URL Format

Use the `Tracking URL` values from:

```text
marketing/facebook-groups/Kromi_50_Verified_Groups_TRACKING.csv
```

Example:

```text
https://kromiuniverse.com/arc?group=fb_001
```

The `group` parameter must match the CRM `Tracking ID`.

## WordPress / Elementor Placement

Recommended placement options, in order:

1. Site-wide custom code manager, limited to the ARC page if possible.
2. Elementor Custom Code with display condition for the ARC page.
3. HTML widget at the bottom of the ARC page.
4. Theme child footer injection, guarded so it runs only on the ARC page.

Use:

```text
website/custom-js/arc-group-tracking.js
```

If adding through Elementor HTML widget, wrap the snippet in:

```html
<script>
/* paste arc-group-tracking.js contents here */
</script>
```

## Hidden Field Setup

Add a hidden field to the ARC signup form:

```text
source_group
```

The JavaScript snippet will populate these selectors:

```text
input[name="source_group"]
input[name="fields[source_group]"]
input[id="source_group"]
input[data-kromi-source-group]
```

If Elementor controls the form directly:

- Add a hidden field.
- Set the field ID/name to `source_group`.
- Leave the default value blank.

If Kit provides the embedded form:

- Confirm the embed supports a hidden custom field.
- Use `source_group` or `fields[source_group]`, depending on Kit's generated markup.
- Verify with browser dev tools before publishing.

## Kit Configuration

In Kit:

1. Create or confirm a custom subscriber field named:

```text
source_group
```

2. Confirm the ARC form submits into that field.
3. Submit a test email from `/arc?group=fb_001`.
4. Confirm the subscriber profile contains:

```text
source_group = fb_001
```

Do not implement Kit API reporting in TASK-002.

## GA4 Configuration

The snippet sends browser events only when `gtag` exists.

Expected events:

- `arc_landing_visit`
- `arc_signup_submit`
- `amazon_click`

Expected event parameter:

```text
source_group
```

Recommended GA4 setup after snippet install:

1. Open GA4 Admin.
2. Create a custom dimension for event parameter `source_group`.
3. Use DebugView or Tag Assistant to verify event payloads.

Do not implement GA4 API reporting in TASK-002.

## Manual Test Plan

### 1. Visit ARC URL

Open:

```text
https://kromiuniverse.com/arc?group=fb_001
```

### 2. Verify Session Storage

In browser console:

```js
sessionStorage.getItem("kromi_source_group")
```

Expected:

```text
fb_001
```

### 3. Verify Fallback Cookie

In browser console:

```js
document.cookie.includes("kromi_source_group=fb_001")
```

Expected:

```text
true
```

### 4. Verify Hidden Field

In browser console:

```js
document.querySelector('input[name="source_group"], input[name="fields[source_group]"]')?.value
```

Expected:

```text
fb_001
```

### 5. Verify Kit Field

Submit the form with a test email address, then confirm in Kit:

```text
source_group = fb_001
```

### 6. Verify GA4 Event Payload

Use GA4 DebugView or Tag Assistant.

Expected event:

```text
arc_landing_visit
```

Expected parameter:

```text
source_group = fb_001
```

Submit the form and confirm:

```text
arc_signup_submit
source_group = fb_001
```

Click an Amazon link and confirm:

```text
amazon_click
source_group = fb_001
```

## Rollback Plan

If tracking causes form or page issues:

1. Remove or disable the custom code block.
2. Clear cache/CDN if applicable.
3. Retest the ARC signup form without the snippet.
4. Re-enable after fixing selector or form markup issues.

## Access Needed

- WordPress admin access or Elementor editor access.
- Confirmation of the production ARC page URL.
- Kit form editor access or the current Kit embed snippet.
- Confirmation that Kit custom field `source_group` exists.
- GA4 DebugView or Tag Assistant access.
- A safe test email address for ARC signup validation.
