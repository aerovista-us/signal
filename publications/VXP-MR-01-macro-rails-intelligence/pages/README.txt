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

The issue ships with `cover.png` as spread 1, then the six cluster PNGs in order (see the manifest).

See `micro_infographic_pack.md` for cluster titles.
