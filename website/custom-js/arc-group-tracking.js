/*
Kromi ARC group tracking

Purpose:
- Capture ?group=fb_001 from the ARC landing page URL.
- Store the value in sessionStorage.
- Store a fallback cookie.
- Populate hidden Kit/ARC form fields.
- Send GA4 event parameters when gtag is available.

This snippet does not call the GA4 API or Kit API directly.
*/

(function () {
  "use strict";

  var PARAM_NAME = "group";
  var STORAGE_KEY = "kromi_source_group";
  var COOKIE_MAX_AGE_SECONDS = 60 * 60 * 24 * 30;
  var GROUP_PATTERN = /^fb_[0-9]{3}$/;
  var FIELD_SELECTORS = [
    'input[name="source_group"]',
    'input[name="fields[source_group]"]',
    'input[id="source_group"]',
    "input[data-kromi-source-group]"
  ];

  function readGroupFromUrl() {
    var params = new URLSearchParams(window.location.search);
    var group = params.get(PARAM_NAME);
    return normalizeGroup(group);
  }

  function normalizeGroup(value) {
    if (!value) return "";
    var group = String(value).trim();
    return GROUP_PATTERN.test(group) ? group : "";
  }

  function cookieIsSecure() {
    return window.location.protocol === "https:";
  }

  function writeCookie(group) {
    if (!group) return;
    var cookie = STORAGE_KEY + "=" + encodeURIComponent(group) +
      "; path=/; max-age=" + COOKIE_MAX_AGE_SECONDS + "; SameSite=Lax";

    if (cookieIsSecure()) {
      cookie += "; Secure";
    }

    document.cookie = cookie;
  }

  function readCookie() {
    var prefix = STORAGE_KEY + "=";
    var cookies = document.cookie ? document.cookie.split(";") : [];

    for (var index = 0; index < cookies.length; index += 1) {
      var item = cookies[index].trim();
      if (item.indexOf(prefix) === 0) {
        return normalizeGroup(decodeURIComponent(item.slice(prefix.length)));
      }
    }

    return "";
  }

  function writeSession(group) {
    if (!group) return false;

    try {
      window.sessionStorage.setItem(STORAGE_KEY, group);
      return true;
    } catch (error) {
      return false;
    }
  }

  function readSession() {
    try {
      return normalizeGroup(window.sessionStorage.getItem(STORAGE_KEY));
    } catch (error) {
      return "";
    }
  }

  function saveGroup(group) {
    if (!group) return;
    writeSession(group);
    writeCookie(group);
  }

  function getActiveGroup() {
    return readSession() || readCookie();
  }

  function populateHiddenFields(group) {
    if (!group) return;

    FIELD_SELECTORS.forEach(function (selector) {
      document.querySelectorAll(selector).forEach(function (input) {
        input.value = group;
        input.setAttribute("value", group);
      });
    });
  }

  function sendGa4Event(eventName, params) {
    if (typeof window.gtag !== "function") return;
    window.gtag("event", eventName, params);
  }

  function trackLandingVisit(group) {
    if (!group) return;

    sendGa4Event("arc_landing_visit", {
      source_group: group,
      page_location: window.location.href,
      page_path: window.location.pathname
    });
  }

  function formIdentifier(form) {
    if (!form) return "unknown";
    return form.getAttribute("id") ||
      form.getAttribute("name") ||
      form.getAttribute("data-form-id") ||
      "arc_signup_form";
  }

  function bindSignupTracking() {
    document.addEventListener("submit", function (event) {
      var group = getActiveGroup();
      if (!group) return;

      var form = event.target;
      populateHiddenFields(group);

      sendGa4Event("arc_signup_submit", {
        source_group: group,
        form_id: formIdentifier(form)
      });
    }, true);
  }

  function bindAmazonClickTracking() {
    document.addEventListener("click", function (event) {
      var link = event.target.closest ? event.target.closest("a") : null;
      if (!link || !link.href) return;

      var href = link.href;
      var isAmazon = href.indexOf("amazon.") !== -1 || href.indexOf("/amazon/") !== -1;
      var group = getActiveGroup();

      if (!isAmazon || !group) return;

      sendGa4Event("amazon_click", {
        source_group: group,
        outbound_url: href
      });
    });
  }

  function observeLateLoadedForms(group) {
    if (!("MutationObserver" in window) || !group) return;

    var observer = new MutationObserver(function () {
      populateHiddenFields(group);
    });

    observer.observe(document.documentElement, {
      childList: true,
      subtree: true
    });
  }

  function initialize() {
    var urlGroup = readGroupFromUrl();
    if (urlGroup) saveGroup(urlGroup);

    var activeGroup = urlGroup || getActiveGroup();
    populateHiddenFields(activeGroup);
    trackLandingVisit(activeGroup);
    bindSignupTracking();
    bindAmazonClickTracking();
    observeLateLoadedForms(activeGroup);

    document.addEventListener("DOMContentLoaded", function () {
      populateHiddenFields(getActiveGroup());
    });
  }

  initialize();
})();
