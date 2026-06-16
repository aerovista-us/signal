# Deploying to GitHub Pages ([aerovista-us/signal](https://github.com/aerovista-us/signal))

Production at [thesignal.aerovista.us](https://thesignal.aerovista.us) serves from the **`main`** branch of this repo. If a file exists on your Collab share but not on GitHub, the live site will 404.

## Fix for `signal-public-theme.css` 404

The homepage (`index.html`) **inlines** the shared theme in a `<style>` block, so pushing only `index.html` restores the newsletter look.

Dispatch pages load **`signal-public-theme.css`** at the **repo root** (not `css/`). That file must be committed and pushed:

```
signal-public-theme.css          ← required for /dispatches/*
css/signal-public-theme.css      ← optional mirror (keep in sync)
index.html
dispatches/*.html
```

## Umami

Set `analytics.websiteId` in [`js/site-config.js`](js/site-config.js) after adding `thesignal.aerovista.us` in Umami. Full checklist (including Cloudflare Access note): [umami-analytics.md](./umami-analytics.md).

## Full sync checklist (local → GitHub)

Copy from `\\100.115.9.61\Collab\mini.shops\thesignal` into your clone of [aerovista-us/signal](https://github.com/aerovista-us/signal), then:

```bash
git add index.html signal-public-theme.css css/signal-public-theme.css js/ dispatches/
git add newsletters/ publications/ docs/ favicon.svg signal.png signal.html
git status
git commit -m "Add shared theme CSS and sync hub/dispatch styles for GitHub Pages."
git push origin main
```

Wait 1–2 minutes for GitHub Pages to rebuild, then hard-refresh the site.

## Link preview image (Slack, iMessage, social)

All hub and dispatch pages use **`signal.png`** at the repo root:

- `og:image` / `twitter:image` → `https://thesignal.aerovista.us/signal.png`
- Do **not** use `singal.png` (typo) or `og-image.jpg` (file does not exist)

After deploy, confirm https://thesignal.aerovista.us/signal.png returns **200**. Chat apps cache previews; re-paste the URL or use [Facebook Sharing Debugger](https://developers.facebook.com/tools/debug/) to refresh.

## Verify after deploy

- https://thesignal.aerovista.us/ — cyan/blue theme, no console 404
- https://thesignal.aerovista.us/signal-public-theme.css — should return CSS (200)
- https://thesignal.aerovista.us/dispatches/eow-shareholder-update.html — themed dispatch page
- https://thesignal.aerovista.us/newsletters/aerovista_signal_weekly_2026-06-15.html — current weekly Signal
- https://thesignal.aerovista.us/newsletters/bytecast-week-ending-2026-06-15.aac — ByteCast audio (or `.mp3` if used)
- https://thesignal.aerovista.us/newsletters/a_high_detail_corporate_infographic_weekly_report.png — weekly infographic
- https://thesignal.aerovista.us/newsletter-current.html — redirect to current newsletter

## What is not on GitHub yet (as of theme work)

These may 404 on production until pushed:

- `publications/` (macro briefing + magazine)
- `docs/`
- Root `signal-public-theme.css` (until next push)
