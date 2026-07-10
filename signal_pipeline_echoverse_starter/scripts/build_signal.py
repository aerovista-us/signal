#!/usr/bin/env python3
"""Build a Signal edition into newsletters/editions/{type}/{slug}/index.html + meta.json."""
from pathlib import Path
import json
import html
import shutil
import argparse
import re

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
CONTENT = ROOT / "content"
ASSETS = ROOT / "assets"
DIST = ROOT / "dist"
EDITIONS_ROOT = REPO / "newsletters" / "editions"
TEMPLATE = ROOT / "templates" / "signal-template.html"
SITE_BASE = "https://thesignal.aerovista.us"


def esc(value):
    return html.escape(str(value), quote=True)


def p(text, cls=None):
    c = f' class="{cls}"' if cls else ""
    return f"<p{c}>{esc(text)}</p>"


def slugify_folder(data):
    if data.get("folderSlug"):
        return data["folderSlug"]
    date = data.get("date", "update")
    slug = data.get("slug", "signal-update")
    short = re.sub(r"-audio-intelligence-platform$", "-echoverse", slug)
    short = re.sub(r"^echoverse-", "", short) if "echoverse" in short else short
    return f"{date}-{short}"


def copy_asset(src_name, out_assets, copied, dest_name=None):
    if not src_name:
        return None
    src = ASSETS / src_name
    if not src.exists():
        return None
    dest = dest_name or src_name
    dest_path = out_assets / dest
    shutil.copy(src, dest_path)
    copied.add(str(dest_path.relative_to(out_assets.parent)))
    return f"assets/{dest}"


def render(content_file, output_root=None, use_dist=False):
    data = json.loads(content_file.read_text(encoding="utf-8"))
    edition_type = data.get("editionType", "milestone")
    folder_slug = slugify_folder(data)
    copied = set()

    if use_dist:
        out_dir = DIST / folder_slug
    elif output_root:
        out_dir = Path(output_root)
    else:
        out_dir = EDITIONS_ROOT / edition_type / folder_slug

    out_assets = out_dir / "assets"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_assets.mkdir(exist_ok=True)

    audio = data.get("audio", {})
    audio_rel = copy_asset(audio.get("file"), out_assets, copied, "audio.mp3") or ""

    visuals_out = []
    for i, visual in enumerate(data.get("visuals", [])):
        file = visual.get("file")
        if file:
            dest = "infographic.png" if i == 0 else f"visual-{i + 1}{Path(file).suffix}"
            rel = copy_asset(file, out_assets, copied, dest)
            if rel:
                visuals_out.append({**visual, "file": rel})

    title = data.get("title", "")
    if "Audio Intelligence Platform" in title:
        title_first = title.replace("Audio Intelligence Platform.", "")
        title_highlight = "Audio Intelligence Platform."
    else:
        parts = title.rsplit(" ", 2)
        title_first = " ".join(parts[:-2]) if len(parts) >= 3 else title
        title_highlight = " ".join(parts[-2:]) if len(parts) >= 3 else ""

    metrics_html = "\n".join(
        f'<div class="metric"><strong>{esc(m.get("value", ""))}</strong><span>{esc(m.get("label", ""))}</span></div>'
        for m in data.get("metrics", [])
    )
    chapters_html = "\n".join(
        f'<div class="chapter"><b>{esc(c.get("time", ""))}</b><span>{esc(c.get("label", ""))}</span></div>'
        for c in audio.get("chapters", [])
    )
    summary_html = "".join(
        p(item, "lede" if i == 0 else None) for i, item in enumerate(data.get("summary", []))
    )
    happy_path_html = "\n".join(
        f'<div class="path-step"><div class="step-num">{esc(s.get("step", ""))}</div><h3>{esc(s.get("title", ""))}</h3><p>{esc(s.get("body", ""))}</p></div>'
        for s in data.get("happyPath", [])
    )
    lanes_html = "\n".join(
        f'<div class="lane"><div class="icon">{esc(l.get("icon", ""))}</div><h3>{esc(l.get("title", ""))}</h3><p>{esc(l.get("body", ""))}</p></div>'
        for l in data.get("lanes", [])
    )
    services_html = "\n".join(
        f'<tr><td>{esc(s.get("component", ""))}</td><td><code>{esc(s.get("endpoint", ""))}</code></td><td><span class="status-pill">{esc(s.get("status", ""))}</span></td></tr>'
        for s in data.get("services", [])
    )
    smoke = data.get("smokeTest", {})
    smoke_items_html = "\n".join(
        f'<b>{esc(i.get("label", ""))}</b><span><code>{esc(i.get("value", ""))}</code></span>'
        for i in smoke.get("items", [])
    )
    quick_reference_html = "\n".join(
        f'<div class="code-row"><code>{esc(cmd)}</code></div>' for cmd in data.get("quickReference", [])
    )
    next_moves_html = "\n".join(
        f'<div class="next-card"><span class="priority {esc(n.get("priority", "P3")).lower()}">{esc(n.get("priority", ""))}</span><h3>{esc(n.get("title", ""))}</h3><p>{esc(n.get("body", ""))}</p></div>'
        for n in data.get("nextMoves", [])
    )
    visuals_html = "\n".join(
        f'<div class="image-card"><img src="{esc(v.get("file", ""))}" alt="{esc(v.get("caption", "Visual"))}" /><p>{esc(v.get("caption", ""))}</p></div>'
        for v in visuals_out
    )
    bottom_line_html = "".join(
        p(item, "lede" if i == 0 else None) for i, item in enumerate(data.get("bottomLine", []))
    )

    canonical = f"{SITE_BASE}/newsletters/editions/{edition_type}/{folder_slug}/"

    replacements = {
        "publication": data.get("publication", "The Signal"),
        "brand": data.get("brand", "AeroVista"),
        "division": data.get("division", "EchoVerse"),
        "date": data.get("date", ""),
        "kicker": data.get("kicker", "Status: Operational"),
        "title_first": title_first.strip(),
        "title_highlight": title_highlight.strip(),
        "subtitle": data.get("subtitle", ""),
        "audio_file": audio_rel,
        "audio_title": audio.get("title", ""),
        "audio_description": audio.get("description", ""),
        "canonical_url": canonical,
        "metrics_html": metrics_html,
        "chapters_html": chapters_html,
        "summary_html": summary_html,
        "quote": data.get("quote", ""),
        "happy_path_html": happy_path_html,
        "lanes_html": lanes_html,
        "services_html": services_html,
        "smoke_title": smoke.get("title", ""),
        "smoke_items_html": smoke_items_html,
        "smoke_note": smoke.get("note", ""),
        "quick_reference_html": quick_reference_html,
        "next_moves_html": next_moves_html,
        "visuals_html": visuals_html,
        "transcript": esc(data.get("transcript", "")),
        "bottom_line_html": bottom_line_html,
        "closing_quote": data.get("closingQuote", ""),
    }

    html_text = TEMPLATE.read_text(encoding="utf-8")
    for key, value in replacements.items():
        html_text = html_text.replace("{{" + key + "}}", str(value))

    index_path = out_dir / "index.html"
    index_path.write_text(html_text, encoding="utf-8")

    meta = {
        "id": f"{edition_type}-{folder_slug}",
        "title": data.get("catalogTitle") or title.replace(".", "").strip(),
        "type": [edition_type],
        "date": data.get("date", ""),
        "href": f"/newsletters/editions/{edition_type}/{folder_slug}/",
        "summary": data.get("subtitle", ""),
        "tags": data.get("tags", []),
        "assets": sorted(copied),
    }
    (out_dir / "meta.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")

    manifest = {
        "output": str(index_path),
        "editionType": edition_type,
        "folderSlug": folder_slug,
        "canonical": canonical,
        "assetsCopied": sorted(copied),
        "source": str(content_file.relative_to(ROOT)),
    }
    (out_dir / "build-manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    if use_dist:
        DIST.mkdir(exist_ok=True)
        (DIST / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    print(f"Built {index_path}")
    print(f"meta.json + {len(copied)} asset(s)")
    return index_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build a Signal edition from JSON content.")
    parser.add_argument("content", nargs="?", default="content/echoverse-platform-update.json")
    parser.add_argument(
        "--dist",
        action="store_true",
        help="Write to signal_pipeline_echoverse_starter/dist/ (legacy)",
    )
    parser.add_argument("--output", help="Override output directory")
    args = parser.parse_args()
    content_file = ROOT / args.content
    if not content_file.exists():
        raise SystemExit(f"Content file not found: {content_file}")
    render(content_file, output_root=args.output, use_dist=args.dist)
