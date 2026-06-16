Optional copy of StPageFlip (npm package `page-flip`) for air-gapped / “no CDN” deploys.

`magazine.mjs` loads the library by fetching JS text and executing it from a blob: URL (same-origin execution).

Default: tries the CDN first, then ./vendor/page-flip.browser.min.js — so an empty vendor folder does not cause a 404.

Prefer local file first: in pages-manifest.json set:

  "preferLocalPageFlip": true

Then populate vendor (once):

  PowerShell: .\publications\VXP-MR-01-macro-rails-intelligence\scripts\pull-page-flip.ps1

Or save manually as vendor/page-flip.browser.min.js from:

  https://cdn.jsdelivr.net/npm/page-flip@2.0.7/dist/js/page-flip.browser.min.js
