# Large edition HTML files

Some ByteCast and shareholder editions embed hero art as **base64 inside CSS** (`url('data:image/png;base64,...')`). These files can exceed 8 MB.

## Do not

- Open the full file in an editor and save wholesale
- Use PowerShell `[System.IO.File]::ReadAllText()` + `WriteAllText()` on the entire file
- Run broad search/replace on short strings that may appear inside base64 payloads (e.g. `a{color:`)

## Do

1. **Binary copy** when replacing the whole file: `Copy-Item -LiteralPath`
2. **Anchored string replace** on unique multi-line HTML blocks (head meta, audio block, nav)
3. **Prefer external assets** for new editions: `assets/hero.png` beside `index.html`
4. Use [`signal_pipeline_echoverse_starter/`](../signal_pipeline_echoverse_starter/) for new pages when possible

## Safe edit checklist

- [ ] Confirm file size before editing (>1 MB → use shell anchors only)
- [ ] After edit: verify `</style>`, `<body>`, and `</html>` still exist
- [ ] Spot-check in browser: hero image, audio player, footer

## Canonical layout

New editions live under `newsletters/editions/{type}/{slug}/` — see [site-structure.md](./site-structure.md).
