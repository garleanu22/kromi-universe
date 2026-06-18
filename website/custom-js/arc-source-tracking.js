/*
Kromi ARC source tracking

Purpose:
- Capture ?group=fb_001 from the ARC page URL
- Store it locally
- Populate hidden form fields when present
- Send basic GA4 events if gtag exists
*/

(function () {
  const PARAM_NAME = 'group';
  const STORAGE_KEY = 'kromi_source_group';
  const FIELD_NAMES = ['source_group', 'group', 'tracking_id'];

  function getGroupFromUrl() {
    const params = new URLSearchParams(window.location.search);
    return params.get(PARAM_NAME);
  }

  function saveGroup(group) {
    if (!group) return;
    try {
      localStorage.setItem(STORAGE_KEY, group);
      document.cookie = `${STORAGE_KEY}=${encodeURIComponent(group)}; path=/; max-age=2592000; SameSite=Lax`;
    } catch (error) {
      console.warn('Kromi tracking storage failed', error);
    }
  }

  function getSavedGroup() {
    try {
      return localStorage.getItem(STORAGE_KEY) || '';
    } catch (error) {
      return '';
    }
  }

  function populateHiddenFields(group) {
    if (!group) return;
    FIELD_NAMES.forEach(function (name) {
      document.querySelectorAll(`input[name="${name}"]`).forEach(function (input) {
        input.value = group;
      });
    });
  }

  function trackPageView(group) {
    if (!group || typeof window.gtag !== 'function') return;
    window.gtag('event', 'arc_source_visit', {
      source_group: group,
      page_location: window.location.href,
    });
  }

  function trackAmazonClicks(group) {
    document.addEventListener('click', function (event) {
      const link = event.target.closest('a');
      if (!link || !link.href) return;

      const isAmazon = link.href.includes('amazon.') || link.href.includes('/amazon/');
      if (!isAmazon || typeof window.gtag !== 'function') return;

      window.gtag('event', 'amazon_click', {
        source_group: group || getSavedGroup(),
        outbound_url: link.href,
      });
    });
  }

  const urlGroup = getGroupFromUrl();
  if (urlGroup) saveGroup(urlGroup);

  const activeGroup = urlGroup || getSavedGroup();
  populateHiddenFields(activeGroup);
  trackPageView(activeGroup);
  trackAmazonClicks(activeGroup);

  document.addEventListener('DOMContentLoaded', function () {
    populateHiddenFields(activeGroup);
  });
})();
