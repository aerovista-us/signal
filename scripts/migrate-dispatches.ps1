# Migrate dispatches into eod/, eow/, topics/ subfolders
param([string]$Root = "\\100.115.9.61\Collab\mini.shops\thesignal")

$Disp = Join-Path $Root "dispatches"
$Base = "https://thesignal.aerovista.us"

function New-RedirectStub {
  param($OldPath, $NewUrl, $Title)
  $rel = $NewUrl.Replace("$Base/", "")
  @"
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta http-equiv="refresh" content="0; url=$rel" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>$Title | The SIGNAL</title>
  <link rel="canonical" href="$NewUrl" />
</head>
<body>
  <p>Redirecting to <a href="$rel">$Title</a>.</p>
</body>
</html>
"@ | Set-Content -LiteralPath $OldPath -Encoding UTF8
}

function Update-DispatchHtml {
  param([string]$Path, [string]$CanonicalUrl)
  $enc = New-Object System.Text.UTF8Encoding $false
  $t = [System.IO.File]::ReadAllText($Path, $enc)
  $t = $t.Replace('../signal-public-theme.css', '/signal-public-theme.css')
  $t = $t.Replace('../favicon.svg', '/favicon.svg')
  $t = $t.Replace('../js/site-config.js', '/js/site-config.js')
  $t = $t.Replace('../js/site-analytics.js', '/js/site-analytics.js')
  $t = $t.Replace('../index.html', '/index.html')
  $t = $t.Replace('../newsletters/', '/newsletters/')
  if ($t -notmatch 'site-paths\.js') {
    $t = $t.Replace('<script src="/js/site-config.js"', '<script src="/js/site-paths.js"></script>' + "`n  " + '<script src="/js/site-config.js"')
  }
  if ($t -match 'rel="canonical" href="[^"]*"') {
    $t = [regex]::Replace($t, 'rel="canonical" href="[^"]*"', "rel=`"canonical`" href=`"$CanonicalUrl`"")
  }
  if ($t -match 'property="og:url" content="[^"]*"') {
    $t = [regex]::Replace($t, 'property="og:url" content="[^"]*"', "property=`"og:url`" content=`"$CanonicalUrl`"")
  }
  [System.IO.File]::WriteAllText($Path, $t, $enc)
}

$moves = @(
  @{ Old = 'eod-current-operating-note.html'; Sub = 'eod'; New = 'current-operating-note.html'; Title = 'Current operating note' },
  @{ Old = 'eow-current-stakeholder-update.html'; Sub = 'eow'; New = 'current-stakeholder-update.html'; Title = 'Current stakeholder update' },
  @{ Old = 'eow-2026-05-29-public-signal.html'; Sub = 'eow'; New = '2026-05-29-public-signal.html'; Title = 'Public Signal May 29' },
  @{ Old = 'eow-2026-05-29-shareholder-report.html'; Sub = 'eow'; New = '2026-05-29-shareholder-report.html'; Title = 'Shareholder report May 29' },
  @{ Old = 'eow-2026-06-28-weekend-report.html'; Sub = 'eow'; New = '2026-06-28-weekend-report.html'; Title = 'Weekend report June 28' },
  @{ Old = 'eow-shareholder-update.html'; Sub = 'eow'; New = 'shareholder-update.html'; Title = 'Shareholder update' },
  @{ Old = 'art-localized-market-update-2026-05-29.html'; Sub = 'topics'; New = 'art-localized-market-update-2026-05-29.html'; Title = 'Art Localized market update' },
  @{ Old = 'av-gear-shop-overlay-cleanup.html'; Sub = 'topics'; New = 'av-gear-shop-overlay-cleanup.html'; Title = 'AV Gear Shop overlay' },
  @{ Old = 'cindy-connect-launch-status.html'; Sub = 'topics'; New = 'cindy-connect-launch-status.html'; Title = 'Cindy Connect launch' },
  @{ Old = 'hydrilla-gorilla-echostory.html'; Sub = 'topics'; New = 'hydrilla-gorilla-echostory.html'; Title = 'Hydrilla Gorilla EchoStory' },
  @{ Old = 'memory-vault-live-avcc.html'; Sub = 'topics'; New = 'memory-vault-live-avcc.html'; Title = 'Memory Vault live AVCC' },
  @{ Old = 'nxcore-resiliency-work-order.html'; Sub = 'topics'; New = 'nxcore-resiliency-work-order.html'; Title = 'NXCore resiliency work order' }
)

foreach ($m in $moves) {
  $subDir = Join-Path $Disp $m.Sub
  New-Item -ItemType Directory -Force -Path $subDir | Out-Null
  $oldPath = Join-Path $Disp $m.Old
  $newPath = Join-Path $subDir $m.New
  if (Test-Path -LiteralPath $oldPath) {
    $content = Get-Content -LiteralPath $oldPath -Raw -ErrorAction SilentlyContinue
    if ($content -match 'http-equiv="refresh"') {
      # already a stub from partial run — skip copy
      Write-Host "Skip stub $($m.Old)"
      continue
    }
    Copy-Item -LiteralPath $oldPath -Destination $newPath -Force
    $canonical = "$Base/dispatches/$($m.Sub)/$($m.New)"
    Update-DispatchHtml -Path $newPath -CanonicalUrl $canonical
    New-RedirectStub -OldPath $oldPath -NewUrl $canonical -Title $m.Title
    Write-Host "Moved $($m.Old) -> dispatches/$($m.Sub)/$($m.New)"
  }
}

# Update internal-signals.html paths (edition URLs)
$hub = Join-Path $Disp 'internal-signals.html'
$enc = New-Object System.Text.UTF8Encoding $false
$h = [System.IO.File]::ReadAllText($hub, $enc)
$replacements = @{
  '../newsletters/aerovista_bytecast_status_player.html' = '/newsletters/editions/eod/2026-07-05-company-status/'
  '../newsletters/bytecast_shareholder_seeing_the_system.html' = '/newsletters/editions/shareholder/2026-07-08-seeing-the-system/'
  '../newsletters/aerovista_weekend_report_6.28.26.html' = '/newsletters/editions/weekly/2026-06-28-resilience-weekend/'
  '../newsletters/aerovista_signal_weekly_2026-06-21.html' = '/newsletters/editions/weekly/2026-06-21-better-machine/'
  '../newsletters/aerovista_signal_weekly_2026-06-15.html' = '/newsletters/editions/weekly/2026-06-15-systems-becoming-products/'
  '../newsletters/aerovista_signal_echoverse_bytecast_2026-06-16.html' = '/newsletters/editions/milestone/2026-06-16-echoverse/'
  '../newsletters/the-signal-newsletter-2026-05-29.html' = '/newsletters/editions/weekly/2026-05-29-newsletter-package/'
  'eod-current-operating-note.html' = '/dispatches/eod/current-operating-note.html'
  'eow-current-stakeholder-update.html' = '/dispatches/eow/current-stakeholder-update.html'
  'eow-2026-06-28-weekend-report.html' = '/dispatches/eow/2026-06-28-weekend-report.html'
  'eow-2026-05-29-shareholder-report.html' = '/dispatches/eow/2026-05-29-shareholder-report.html'
  'eow-2026-05-29-public-signal.html' = '/dispatches/eow/2026-05-29-public-signal.html'
  'eow-shareholder-update.html' = '/dispatches/eow/shareholder-update.html'
  'https://thesignal.aerovista.us/newsletters/aerovista_bytecast_status_player.html' = 'https://thesignal.aerovista.us/newsletters/editions/eod/2026-07-05-company-status/'
}
foreach ($k in $replacements.Keys) { $h = $h.Replace($k, $replacements[$k]) }
$h = $h.Replace('../signal-public-theme.css', '/signal-public-theme.css')
$h = $h.Replace('../favicon.svg', '/favicon.svg')
$h = $h.Replace('../js/site-config.js', '/js/site-config.js')
$h = $h.Replace('../js/site-analytics.js', '/js/site-analytics.js')
$h = $h.Replace('../index.html', '/index.html')
if ($h -notmatch 'site-paths\.js') {
  $h = $h.Replace('<script src="/js/site-config.js"', '<script src="/js/site-paths.js"></script>' + "`n  " + '<script src="/js/site-config.js"')
}
[System.IO.File]::WriteAllText($hub, $h, $enc)

Write-Host "Phase 3 dispatch migration complete."
