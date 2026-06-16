# Umami analytics — The SIGNAL

## Config shape

[`js/site-config.js`](../js/site-config.js):

```javascript
analytics: {
  provider: "umami",
  enabled: true,
  scriptUrl: "https://analytics.aerovista.us/script.js",
  websiteId: "paste-uuid-here",
}
```

If `websiteId` is empty, the loader logs `Umami skipped: missing websiteId` and does not inject the script.

## Deploy checklist

1. Add `thesignal.aerovista.us` in Umami (**Websites → Add website**).
2. Paste the UUID into `js/site-config.js` → `analytics.websiteId`.
3. Push `js/` + updated HTML to GitHub.
4. Deploy GitHub Pages / site.
5. Open Umami → **Realtime**.
6. Click through hub, publication pages, and archive links.

## Verify

1. Visit https://thesignal.aerovista.us/
2. DevTools → **Console** — should not show the skip message once UUID is set.
3. DevTools → **Network** — filter `script.js` and `send`; tracker should load and `/api/send` return **200**.
4. Umami **Realtime** should show your session while you click around.

## Script domain must be public

`scriptUrl` must be reachable from visitors’ browsers. If `analytics.aerovista.us` sits behind **Cloudflare Access** (or similar), the tracker may fail silently on the public site. Either expose `/script.js` and `/api/send` without auth, or use a public Umami host for production tracking.

## Events tracked

| Event | When |
|-------|------|
| Page views | Automatic (Umami default) |
| `cta_read_latest` | Hero “Read latest dispatch” |
| `cta_subscribe` | Hero “Get updates” |
| `cta_subscribe_submit` | Subscribe button click |
| `subscribe_submit` | Subscribe form submit |
| `dispatch_open` | Dispatch card “Open dispatch” |
| `publication_open` | Publication card links |
| `filter_category` | Archive category chip click |

## Files

- [`js/site-config.js`](../js/site-config.js) — provider, URLs, website ID
- [`js/site-analytics.js`](../js/site-analytics.js) — loader + event helpers

Included on: `index.html`, all `dispatches/*.html`, `signal.html`, and publication HTML under `publications/`.
