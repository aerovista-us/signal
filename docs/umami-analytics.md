# Umami analytics — The SIGNAL

## One-time setup

1. Open your Umami dashboard (same instance used for other AeroVista sites).
2. **Websites → Add website**
   - Name: `The SIGNAL`
   - Domain: `thesignal.aerovista.us`
3. Copy the **website ID** from the tracking snippet.
4. Paste it in [`js/site-config.js`](../js/site-config.js):

```javascript
websiteId: "your-uuid-here",
```

5. Confirm `scriptUrl` matches your instance (default: `https://analytics.aerovista.us/script.js`).
6. Deploy `js/` folder to GitHub with the rest of the site.

## Verify

1. Visit https://thesignal.aerovista.us/
2. Open DevTools → Network → filter `send` or `script.js`
3. You should see the tracker load and `/api/send` return **200**
4. In Umami, open **Realtime** while clicking around

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

- [`js/site-config.js`](../js/site-config.js) — IDs and URLs
- [`js/site-analytics.js`](../js/site-analytics.js) — loader + event helpers

Included on: `index.html`, all `dispatches/*.html`, `signal.html`, and VXP-MR-01 publication HTML.
