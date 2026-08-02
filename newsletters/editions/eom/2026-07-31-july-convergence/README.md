# AeroVista July 2026 Interactive Month-End Signal

Open `index.html` to start.

## Structure

- `index.html` — interactive overview/home page
- `reports/` — six drill-down report pages
- `bytecasts/` — complete ByteCast transcript series
- `audio/` — place final MP3 files here using the included filenames
- `sources/` — original Markdown reports and uploaded evidence
- `assets/` — styles, JavaScript and images
- `report-index.json` — machine-readable report map

## Audio

The site is fully usable without audio. Players look for the six filenames listed in `audio/README.txt`. When the MP3s are added, no HTML changes are required.

## Deployment

The package is static and can be served from GitHub Pages, Firebase Hosting, nginx, or the AeroVista internal Signal site. Preserve the folder structure so report, source, image and audio links continue to work.
