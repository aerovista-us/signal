# Migrate newsletter editions to newsletters/editions/{type}/{slug}/
param([string]$Root = "\\100.115.9.61\Collab\mini.shops\thesignal")

$Base = "https://thesignal.aerovista.us"
$News = Join-Path $Root "newsletters"
$Editions = Join-Path $News "editions"

function New-RedirectStub {
  param($OldPath, $NewUrl, $Title)
  $rel = $NewUrl.Replace("$Base/newsletters/", "")
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

function Update-EditionHtml {
  param([string]$Path, [string]$CanonicalUrl, [hashtable]$AssetMap)
  $enc = New-Object System.Text.UTF8Encoding $false
  $t = [System.IO.File]::ReadAllText($Path, $enc)
  $t = $t.Replace('../favicon.svg', '/favicon.svg')
  $t = $t.Replace('../js/site-config.js', '/js/site-config.js')
  $t = $t.Replace('../js/site-analytics.js', '/js/site-analytics.js')
  if ($t -notmatch 'site-paths\.js') {
    $t = $t.Replace('<script src="/js/site-config.js"', '<script src="/js/site-paths.js"></script>' + "`n  " + '<script src="/js/site-config.js"')
  }
  $t = $t.Replace('../dispatches/internal-signals.html', '/dispatches/internal-signals.html')
  $t = $t.Replace('../index.html', '/index.html')
  $t = $t.Replace('href="../index.html"', 'href="/index.html"')
  foreach ($k in $AssetMap.Keys) {
    $t = $t.Replace($k, $AssetMap[$k])
  }
  if ($t -match 'rel="canonical" href="[^"]*"') {
    $t = [regex]::Replace($t, 'rel="canonical" href="[^"]*"', "rel=`"canonical`" href=`"$CanonicalUrl`"")
  }
  if ($t -match 'property="og:url" content="[^"]*"') {
    $t = [regex]::Replace($t, 'property="og:url" content="[^"]*"', "property=`"og:url`" content=`"$CanonicalUrl`"")
  }
  [System.IO.File]::WriteAllText($Path, $t, $enc)
}

$migrations = @(
  @{
    OldHtml = 'aerovista_signal_weekly_2026-06-15.html'
    Type = 'weekly'; Slug = '2026-06-15-systems-becoming-products'
    Title = 'Systems Becoming Products'
    Assets = @{
      'bytecast-week-ending-2026-06-15.mp3' = @{ Src = 'bytecast-week-ending-2026-06-15.mp3'; Dest = 'assets/audio.mp3' }
      'bytecast-week-ending-2026-06-15.wav' = @{ Src = 'bytecast-week-ending-2026-06-15.wav'; Dest = 'assets/audio.wav' }
      'a_high_detail_corporate_infographic_weekly_report.png' = @{ Src = 'a_high_detail_corporate_infographic_weekly_report.png'; Dest = 'assets/infographic.png' }
    }
    Map = @{
      'bytecast-week-ending-2026-06-15.mp3' = 'assets/audio.mp3'
      'bytecast-week-ending-2026-06-15.wav' = 'assets/audio.wav'
      'a_high_detail_corporate_infographic_weekly_report.png' = 'assets/infographic.png'
      'https://thesignal.aerovista.us/newsletters/a_high_detail_corporate_infographic_weekly_report.png' = 'https://thesignal.aerovista.us/newsletters/editions/weekly/2026-06-15-systems-becoming-products/assets/infographic.png'
    }
  },
  @{
    OldHtml = 'aerovista_signal_weekly_2026-06-21.html'
    Type = 'weekly'; Slug = '2026-06-21-better-machine'
    Title = 'A Better Machine'
    Assets = @{
      'bytecasewe621.mp3' = @{ Src = 'bytecasewe621.mp3'; Dest = 'assets/audio.mp3' }
      'WEjune21.png' = @{ Src = 'WEjune21.png'; Dest = 'assets/infographic.png' }
    }
    Map = @{
      'bytecasewe621.mp3' = 'assets/audio.mp3'
      'WEjune21.png' = 'assets/infographic.png'
      'https://thesignal.aerovista.us/newsletters/WEjune21.png' = 'https://thesignal.aerovista.us/newsletters/editions/weekly/2026-06-21-better-machine/assets/infographic.png'
    }
  },
  @{
    OldHtml = 'aerovista_weekend_report_6.28.26.html'
    Type = 'weekly'; Slug = '2026-06-28-resilience-weekend'
    Title = 'Resilience Weekend'
    Assets = @{
      'weekend-report.mp3' = @{ Src = 'weekend-report.mp3'; Dest = 'assets/audio.mp3' }
      'weekend-report.aac' = @{ Src = 'weekend-report.aac'; Dest = 'assets/audio.aac' }
    }
    Map = @{
      './weekend-report.mp3' = 'assets/audio.mp3'
      'weekend-report.mp3' = 'assets/audio.mp3'
    }
  },
  @{
    OldHtml = 'aerovista_signal_echoverse_bytecast_2026-06-16.html'
    Type = 'milestone'; Slug = '2026-06-16-echoverse'
    Title = 'EchoVerse Audio Intelligence'
    Assets = @{
      'echoverse-bytecast-2026-06-16.mp3' = @{ Src = 'echoverse-bytecast-2026-06-16.mp3'; Dest = 'assets/audio.mp3' }
      'EchoVerse Platform Shift.mp3' = @{ Src = 'EchoVerse Platform Shift.mp3'; Dest = 'assets/audio-alt.mp3' }
      'a_detailed_infographic_poster_dashboard_style_de.png' = @{ Src = 'a_detailed_infographic_poster_dashboard_style_de.png'; Dest = 'assets/infographic.png' }
      'echoverse_bytecast_transcript_2026-06-16.txt' = @{ Src = 'echoverse_bytecast_transcript_2026-06-16.txt'; Dest = 'assets/transcript.txt' }
    }
    Map = @{
      'echoverse-bytecast-2026-06-16.mp3' = 'assets/audio.mp3'
      'EchoVerse Platform Shift.mp3' = 'assets/audio-alt.mp3'
      'a_detailed_infographic_poster_dashboard_style_de.png' = 'assets/infographic.png'
    }
  },
  @{
    OldHtml = 'aerovista_bytecast_status_player.html'
    Type = 'eod'; Slug = '2026-07-05-company-status'
    Title = 'Overall Company Status'
    Assets = @{
      '7.5.26.EOD.mp3' = @{ Src = '7.5.26.EOD.mp3'; Dest = 'assets/audio.mp3' }
      'overallstatus.png' = @{ Src = 'overallstatus.png'; Dest = 'assets/infographic.png' }
    }
    Map = @{
      '7.5.26.EOD.mp3' = 'assets/audio.mp3'
      'overallstatus.png' = 'assets/infographic.png'
      'https://thesignal.aerovista.us/newsletters/overallstatus.png' = 'https://thesignal.aerovista.us/newsletters/editions/eod/2026-07-05-company-status/assets/infographic.png'
    }
  },
  @{
    OldHtml = 'bytecast_shareholder_seeing_the_system.html'
    Type = 'shareholder'; Slug = '2026-07-08-seeing-the-system'
    Title = 'Seeing the System'
    Assets = @{
      'bytecast-build-nevada.mp3' = @{ Src = 'bytecast-build-nevada.mp3'; Dest = 'assets/audio.mp3' }
      'bytecast-build_navada.mp3' = @{ Src = 'bytecast-build_navada.mp3'; Dest = 'assets/audio-legacy-navada.mp3' }
    }
    Map = @{
      'bytecast-build-nevada.mp3' = 'assets/audio.mp3'
      'bytecast-build_navada.mp3' = 'assets/audio-legacy-navada.mp3'
      'https://thesignal.aerovista.us/newsletters/bytecast-build-nevada.mp3' = 'https://thesignal.aerovista.us/newsletters/editions/shareholder/2026-07-08-seeing-the-system/assets/audio.mp3'
      'https://thesignal.aerovista.us/newsletters/bytecast-build_navada.mp3' = 'https://thesignal.aerovista.us/newsletters/editions/shareholder/2026-07-08-seeing-the-system/assets/audio.mp3'
    }
  },
  @{
    OldHtml = 'the-signal-newsletter-2026-05-29.html'
    Type = 'weekly'; Slug = '2026-05-29-newsletter-package'
    Title = 'Newsletter Package May 29'
    Assets = @{}
    Map = @{}
  }
)

foreach ($m in $migrations) {
  $destDir = Join-Path (Join-Path $Editions $m.Type) $m.Slug
  $assetsDir = Join-Path $destDir 'assets'
  New-Item -ItemType Directory -Force -Path $assetsDir | Out-Null

  $oldPath = Join-Path $News $m.OldHtml
  $indexPath = Join-Path $destDir 'index.html'
  Copy-Item -LiteralPath $oldPath -Destination $indexPath -Force

  foreach ($a in $m.Assets.Values) {
    $srcPath = Join-Path $News $a.Src
    $dstPath = Join-Path $destDir $a.Dest
    if (Test-Path -LiteralPath $srcPath) {
      New-Item -ItemType Directory -Force -Path (Split-Path $dstPath) | Out-Null
      Copy-Item -LiteralPath $srcPath -Destination $dstPath -Force
    }
  }

  $canonical = "$Base/newsletters/editions/$($m.Type)/$($m.Slug)/"
  Update-EditionHtml -Path $indexPath -CanonicalUrl $canonical -AssetMap $m.Map

  $meta = @{
    id = "$($m.Type)-$($m.Slug)"
    title = $m.Title
    type = @($m.Type)
    date = if ($m.Slug -match '^(\d{4}-\d{2}-\d{2})') { $Matches[1] } else { '' }
    href = "/newsletters/editions/$($m.Type)/$($m.Slug)/"
    legacyHref = "/newsletters/$($m.OldHtml)"
    summary = ''
  } | ConvertTo-Json -Depth 4
  $meta | Set-Content -LiteralPath (Join-Path $destDir 'meta.json') -Encoding UTF8

  New-RedirectStub -OldPath $oldPath -NewUrl $canonical -Title $m.Title
  Write-Host "Migrated $($m.OldHtml) -> editions/$($m.Type)/$($m.Slug)/"
}

# EchoVerse legacy stubs
$evoCanonical = "$Base/newsletters/editions/milestone/2026-06-16-echoverse/"
foreach ($stub in @(
  'aerovista_signal_echoverse_audio_intelligence_update_2026-06-16.html',
  'aerovista_signal_echoverse_audio_intelligence_update_enhanced_2026-06-16.html'
)) {
  New-RedirectStub -OldPath (Join-Path $News $stub) -NewUrl $evoCanonical -Title 'EchoVerse ByteCast'
}

Write-Host "Phase 2 migration complete."
