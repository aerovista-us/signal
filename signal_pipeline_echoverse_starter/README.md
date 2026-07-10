# Signal Pipeline Starter

A repeatable page generator for AeroVista Signal updates.

## What it does

Drop in:
- one JSON content file
- one audio file
- one or more visuals

Run one command and get:
- polished Signal HTML page
- audio player
- sticky player
- chapters
- transcript
- metrics
- happy path
- status table
- next steps
- visual brief

## Build

```bash
cd signal_pipeline_echoverse_starter
python scripts/build_signal.py
```

Output defaults to:

```txt
newsletters/editions/{editionType}/{folderSlug}/
  index.html
  meta.json
  assets/
```

Legacy `dist/` output: `python scripts/build_signal.py --dist`

## Create a new Signal page

1. Copy `content/echoverse-platform-update.json`
2. Set `editionType` (`weekly`, `eod`, `bytecast`, `milestone`, `shareholder`), `date`, `folderSlug`, `catalogTitle`, `tags`
3. Drop audio and images into `assets/`
4. Run `python scripts/build_signal.py content/YOUR_FILE.json`
5. Add an entry to `js/signals-catalog.json` and deploy

## Recommended publishing flow

```txt
Session Report → ByteCast script → Audio render → Infographic → JSON content
→ build_signal.py → newsletters/editions/... → catalog JSON → deploy
```
