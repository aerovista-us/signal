# One-time: download page-flip browser bundle (same-origin; avoids Tracking Prevention on CDN scripts).
$ErrorActionPreference = "Stop"
$issueRoot = Split-Path -Parent $PSScriptRoot
$out = Join-Path $issueRoot "vendor/page-flip.browser.min.js"
New-Item -ItemType Directory -Force -Path (Split-Path $out) | Out-Null
Invoke-WebRequest -Uri "https://cdn.jsdelivr.net/npm/page-flip@2.0.7/dist/js/page-flip.browser.min.js" -OutFile $out -UseBasicParsing
Write-Host "Wrote $((Get-Item $out).Length) bytes -> $out"
