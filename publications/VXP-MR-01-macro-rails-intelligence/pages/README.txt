PNG magazine pages for `magazine.html`
=====================================

Edit `../pages-manifest.json`.

Root (optional): `title` (main header line; if omitted, `issue` is shown), `partner`, `issue` — used in the magazine header.

Each item in `pages` can be:

  • A string — relative path to a PNG (next to `magazine.html` or under `pages/`).

  • An object with art + copy for the header / chin:
      `{ "src": "volume_02_….png", "title": "…", "note": "…", "links": [ { "label": "…", "href": "./volume_02_….md" } ] }`

  • `{ "placeholder": true, "label": "…" }` — optional `title`, `note`, `links` if you want chin text before the PNG exists.

`href` values are sanitized (`javascript:` / `data:` blocked). Same-origin links open in the same tab.

The issue ships with five magazine spreads (see `pages-manifest.json`):

  1. `cover.png` — daily convergence brief (page 1 of 6 in art)
  2. `02_signal_clusters_deep_dive.png` — four convergence zones
  3. `03_05_convergence_architecture.png` — global convergence + financial OS + risk matrix (art pages 3–5)
  4. `06_07_strategic_outlook.png` — strategic outlook + daily watch (art pages 6–7)
  5. `back_cover.png`

Legacy cluster PNGs (`volume_*.png`, `01.regulartory…`, etc.) may remain on disk for reference but are not in the active manifest.

See `micro_infographic_pack.md` for cluster titles.
