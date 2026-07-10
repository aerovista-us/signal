/**
 * The SIGNAL — site-wide config (analytics, sharing).
 * In Umami: Websites → Add → thesignal.aerovista.us → paste website ID below.
 * Paths: see site-paths.js (SIGNAL_PATHS).
 */
(function () {
  var base = (window.SIGNAL_PATHS && window.SIGNAL_PATHS.root) || "/";
  var og = (window.SIGNAL_PATHS && window.SIGNAL_PATHS.ogImage) || "/signal.png";
  if (og.charAt(0) === "/") {
    og = "https://thesignal.aerovista.us" + og;
  }
  window.SIGNAL_SITE = {
  url: "https://thesignal.aerovista.us",
  name: "The SIGNAL",
  ogImage: og,
  analytics: {
    provider: "umami",
    enabled: true,
    scriptUrl: "https://analytics.aerovista.us/script.js",
    /** Paste from Umami → Websites → The SIGNAL → Tracking code */
    websiteId: "",
  },
};
})();
