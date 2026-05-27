/**
 * Umami loader + lightweight event helpers for The SIGNAL.
 * Requires js/site-config.js first.
 */
(function () {
  const cfg = window.SIGNAL_SITE || {};
  const umami = cfg.umami || {};

  function loadUmami() {
    if (!umami.enabled || !umami.scriptUrl || !umami.websiteId) return;
    if (document.querySelector('script[data-website-id="' + umami.websiteId + '"]')) return;

    const s = document.createElement("script");
    s.defer = true;
    s.async = true;
    s.src = umami.scriptUrl;
    s.setAttribute("data-website-id", umami.websiteId);
    s.setAttribute("data-domains", "thesignal.aerovista.us");
    document.head.appendChild(s);
  }

  window.signalTrack = function (name, data) {
    if (typeof window.umami === "function") {
      window.umami(name, data);
    }
  };

  function bindCtaTracking() {
    document.querySelectorAll("[data-track]").forEach(function (el) {
      el.addEventListener("click", function () {
        signalTrack(el.getAttribute("data-track"), {
          label: el.getAttribute("data-track-label") || "",
          href: el.getAttribute("href") || "",
        });
      });
    });
  }

  function bindSubscribeForm() {
    const form = document.querySelector(".subscribe-form");
    if (!form) return;
    form.addEventListener("submit", function () {
      signalTrack("subscribe_submit");
    });
  }

  function showSubscribeThanks() {
    if (!/subscribed=1/.test(location.search + location.hash)) return;
    const box = document.querySelector(".subscribe-thanks");
    if (box) box.hidden = false;
  }

  loadUmami();
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", function () {
      bindCtaTracking();
      bindSubscribeForm();
      showSubscribeThanks();
    });
  } else {
    bindCtaTracking();
    bindSubscribeForm();
    showSubscribeThanks();
  }
})();
