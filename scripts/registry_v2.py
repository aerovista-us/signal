#!/usr/bin/env python3
"""Signal Registry v2 validator, manifest refresher, index builder, and UI catalog generator."""

from __future__ import annotations

import argparse
import hashlib
import json
import mimetypes
import re
import subprocess
from datetime import date, datetime
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "registry"
RECORDS = REGISTRY / "records"
INDEXES = REGISTRY / "indexes"
PRESENTATION = REGISTRY / "presentation" / "signals-catalog.json"
CATALOG_OUT = ROOT / "js" / "signals-catalog.json"

REQUIRED = {
    "schemaVersion","id","contentClass","title","summary","owner","status",
    "audience","formats","issuedAt","canonicalUrl","canonicalPath","tags","package","files"
}
CLASSES = {"report","publication","dispatch","media"}
STATUSES = {"draft","review","final","superseded","withdrawn"}
RELATIONSHIPS = {"owned","referenced"}
REPORT_CLASSES = {"eod","eow","mtd","eom","quarterly","annual","milestone","incident","audit","compliance","release-readiness","production-validation","investigation","risk-review","special"}
AUDIENCES = {"internal","executive","operations","staff","stakeholder","shareholder","advisor","partner","public","client","community"}
ROLES = {"primary","report-section","audio","video","image","document","transcript","source","data","metadata","style","script","readme","redirect","evidence","attachment","other"}
PACKAGE_MODES = {"directory","legacy-flat","external"}
ID_RE = re.compile(r"^AV-[A-Z]+-[A-Z0-9-]+$")
REPORT_ID_RE = re.compile(r"^AV-RPT-[A-Z0-9-]+$")
SHA1_RE = re.compile(r"^[0-9a-f]{40}$")
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
INDEX_NAMES = {
    "report": "reports.json",
    "publication": "publications.json",
    "dispatch": "dispatches.json",
    "media": "media.json",
}

def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))

def write_json(path: Path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

def load_records():
    records = []
    for path in sorted(RECORDS.glob("*/*.json")):
        obj = read_json(path)
        obj["_recordPath"] = path.relative_to(ROOT).as_posix()
        records.append(obj)
    return records

def safe_repo_path(value: str):
    if not isinstance(value, str) or not value:
        return False
    p = Path(value)
    return not p.is_absolute() and ".." not in p.parts

def git_blob_sha1(path: Path):
    cp = subprocess.run(["git","hash-object",str(path)], cwd=ROOT, text=True, capture_output=True)
    return cp.stdout.strip() if cp.returncode == 0 else None

def sha256_file(path: Path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def file_type(path: Path):
    return path.suffix.lower().lstrip(".") or "file"

def media_type(path: Path):
    mt, _ = mimetypes.guess_type(path.name)
    if mt:
        return mt
    return {
        ".md": "text/markdown",
        ".mjs": "text/javascript",
        ".yaml": "application/yaml",
        ".yml": "application/yaml",
        ".aac": "audio/aac",
        ".wav": "audio/wav",
    }.get(path.suffix.lower(), "application/octet-stream")

def infer_role(path: Path):
    p = path.as_posix().lower()
    ext = path.suffix.lower()
    name = path.name.lower()
    if name in {"index.html","issue.html","magazine.html","signals_briefing.html"}:
        return "primary"
    if name.startswith("meta.") or "manifest" in name or name.endswith("_meta.yaml") or name.endswith("_meta.yml"):
        return "metadata"
    if "readme" in name:
        return "readme"
    if ext in {".mp3",".aac",".wav",".m4a"}:
        return "audio"
    if ext in {".mp4",".mov",".webm"}:
        return "video"
    if ext in {".png",".jpg",".jpeg",".webp",".gif",".svg"}:
        return "image"
    if ext == ".css":
        return "style"
    if ext in {".js",".mjs",".ps1",".py"}:
        return "script"
    if name == "bytecast.html":
        return "report-section"
    if "transcript" in p or "bytecast" in p:
        return "transcript"
    if "/reports/" in p and ext in {".html",".md"}:
        return "report-section"
    if "/sources/" in p or "appendix" in name or ext == ".md":
        return "source"
    if ext in {".json",".csv"}:
        return "data"
    if ext in {".pdf",".docx",".xlsx",".pptx",".rtf"}:
        return "document"
    return "other"

def stable_file_id(rel_path: str):
    s = re.sub(r"[^a-z0-9]+", "-", rel_path.lower()).strip("-")
    return s[:120] or "file"

def enrich_file_entry(entry):
    e = dict(entry)
    rel = Path(e["path"])
    full = ROOT / rel
    e.setdefault("name", rel.name)
    e.setdefault("fileType", file_type(rel))
    e.setdefault("mediaType", media_type(rel))
    if full.is_file():
        e["sizeBytes"] = full.stat().st_size
        integ = dict(e.get("integrity") or {})
        blob = git_blob_sha1(full)
        if blob:
            integ["gitBlobSha1"] = blob
        integ["sha256"] = sha256_file(full)
        e["integrity"] = integ
    return e

def scan_package(record):
    package = record.get("package") or {}
    root_rel = package.get("root")
    if package.get("mode") != "directory" or not safe_repo_path(root_rel):
        return None
    package_root = ROOT / root_rel
    if not package_root.is_dir():
        return None

    existing_refs = [f for f in record.get("files", []) if f.get("relationship") == "referenced"]
    owned = []
    for full in sorted(p for p in package_root.rglob("*") if p.is_file()):
        rel = full.relative_to(ROOT).as_posix()
        local = full.relative_to(package_root)
        owned.append(enrich_file_entry({
            "id": stable_file_id(local.as_posix()),
            "role": infer_role(local),
            "relationship": "owned",
            "path": rel,
            "name": full.name,
            "fileType": file_type(full),
            "mediaType": media_type(full),
        }))
    return owned + [enrich_file_entry(f) for f in existing_refs]

def refresh_records():
    changed = 0
    for path in sorted(RECORDS.glob("*/*.json")):
        record = read_json(path)
        if record.get("contentClass") == "report":
            record["reportId"] = record["id"]

        scanned = scan_package(record)
        if scanned is not None:
            record["files"] = scanned
        else:
            record["files"] = [enrich_file_entry(f) for f in record.get("files", [])]

        before = path.read_text(encoding="utf-8-sig")
        after = json.dumps(record, indent=2, ensure_ascii=False) + "\n"
        if before != after:
            path.write_text(after, encoding="utf-8")
            changed += 1
    return changed

def parse_date(value, label, errors, rp):
    try:
        return date.fromisoformat(value)
    except Exception:
        errors.append(f"{rp}: {label} must be YYYY-MM-DD")
        return None

def validate_period(record, rp, errors):
    if record.get("contentClass") != "report":
        return
    period = record.get("period")
    if not isinstance(period, dict) or not period:
        errors.append(f"{rp}: period required for reports")
        return
    extras = set(period) - {"start","end","effectiveAt"}
    if extras:
        errors.append(f"{rp}: invalid period fields {sorted(extras)}")
    has_range = "start" in period or "end" in period
    has_effective = "effectiveAt" in period
    if not has_range and not has_effective:
        errors.append(f"{rp}: period requires start/end or effectiveAt")
    if has_range:
        if not period.get("start") or not period.get("end"):
            errors.append(f"{rp}: period start and end must be provided together")
        else:
            start = parse_date(period["start"], "period.start", errors, rp)
            end = parse_date(period["end"], "period.end", errors, rp)
            issued = parse_date(record.get("issuedAt",""), "issuedAt", errors, rp)
            if start and end and start > end:
                errors.append(f"{rp}: period.start must be <= period.end")
            if issued and end and record.get("status") == "final" and issued < end:
                errors.append(f"{rp}: final issuedAt cannot be before period.end")
    if has_effective:
        try:
            datetime.fromisoformat(period["effectiveAt"].replace("Z","+00:00"))
        except Exception:
            errors.append(f"{rp}: period.effectiveAt must be ISO-8601 date-time")

def validate(records):
    errors = []
    ids = set()
    globally_owned = {}

    for r in records:
        rp = r["_recordPath"]
        missing = REQUIRED - set(r)
        if missing:
            errors.append(f"{rp}: missing required fields: {sorted(missing)}")
            continue

        rid = r.get("id")
        if r.get("schemaVersion") != "2.0":
            errors.append(f"{rp}: schemaVersion must be 2.0")
        if not isinstance(rid,str) or not ID_RE.fullmatch(rid):
            errors.append(f"{rp}: invalid id format {rid!r}")
        elif rid in ids:
            errors.append(f"{rp}: duplicate id {rid}")
        ids.add(rid)

        cls = r.get("contentClass")
        if cls not in CLASSES:
            errors.append(f"{rp}: invalid contentClass {cls!r}")
        if r.get("status") not in STATUSES:
            errors.append(f"{rp}: invalid status {r.get('status')!r}")
        for field in ("title","owner","canonicalUrl","canonicalPath"):
            if not isinstance(r.get(field),str) or not r[field].strip():
                errors.append(f"{rp}: {field} must be non-empty")
        if not isinstance(r.get("summary"),str):
            errors.append(f"{rp}: summary must be a string")

        if not safe_repo_path(r.get("canonicalPath","")):
            errors.append(f"{rp}: canonicalPath must be repository-relative and cannot contain ..")
        else:
            canonical = ROOT / r["canonicalPath"]
            if not canonical.is_file():
                errors.append(f"{rp}: canonicalPath does not exist: {r['canonicalPath']}")

        if isinstance(r.get("canonicalUrl"),str) and not r["canonicalUrl"].startswith(("https://","http://")):
            errors.append(f"{rp}: canonicalUrl must be absolute http(s)")

        audience = r.get("audience")
        if not isinstance(audience,list) or not audience or len(audience) != len(set(audience)):
            errors.append(f"{rp}: audience must be a non-empty unique array")
        else:
            unknown = sorted(set(audience) - AUDIENCES)
            if unknown:
                errors.append(f"{rp}: invalid audience values {unknown}")

        formats = r.get("formats")
        if not isinstance(formats,list) or not formats or len(formats) != len(set(formats)) or any(not isinstance(x,str) or not x for x in formats):
            errors.append(f"{rp}: formats must be a non-empty unique string array")

        tags = r.get("tags")
        if not isinstance(tags,list) or len(tags) != len(set(tags)) or any(not isinstance(x,str) or not x for x in tags):
            errors.append(f"{rp}: tags must be a unique string array")

        parse_date(r.get("issuedAt",""), "issuedAt", errors, rp)

        if cls == "report":
            report_id = r.get("reportId")
            if not isinstance(report_id,str) or not REPORT_ID_RE.fullmatch(report_id):
                errors.append(f"{rp}: valid reportId required for reports")
            elif report_id != rid:
                errors.append(f"{rp}: reportId must equal id")
            if r.get("reportClass") not in REPORT_CLASSES:
                errors.append(f"{rp}: invalid or missing reportClass")
        elif cls == "publication":
            if not isinstance(r.get("publicationClass"),str) or not r["publicationClass"].strip():
                errors.append(f"{rp}: publicationClass required for publications")
        validate_period(r, rp, errors)

        package = r.get("package")
        if not isinstance(package,dict):
            errors.append(f"{rp}: package must be an object")
            package = {}
        else:
            if package.get("mode") not in PACKAGE_MODES:
                errors.append(f"{rp}: invalid package.mode")
            if not safe_repo_path(package.get("root","")):
                errors.append(f"{rp}: package.root must be repository-relative and safe")
            if not isinstance(package.get("strict"),bool) or not isinstance(package.get("portable"),bool):
                errors.append(f"{rp}: package.strict and package.portable must be booleans")

        files = r.get("files")
        if not isinstance(files,list) or not files:
            errors.append(f"{rp}: files must be a non-empty array")
            continue

        file_ids = set()
        owned_paths = set()
        primary_owned = []
        for f in files:
            if not isinstance(f,dict):
                errors.append(f"{rp}: file entries must be objects")
                continue
            req = {"id","role","relationship","path","name","fileType","mediaType","sizeBytes","integrity"}
            fm = req - set(f)
            if fm:
                errors.append(f"{rp}: file entry missing {sorted(fm)}")
                continue

            fid = f.get("id")
            if not isinstance(fid,str) or not fid:
                errors.append(f"{rp}: file id must be non-empty")
            elif fid in file_ids:
                errors.append(f"{rp}: duplicate file id {fid}")
            file_ids.add(fid)

            if f.get("role") not in ROLES:
                errors.append(f"{rp}: invalid file role {f.get('role')!r} for {f.get('path')}")
            if f.get("relationship") not in RELATIONSHIPS:
                errors.append(f"{rp}: invalid relationship for {f.get('path')}")
                continue
            if not safe_repo_path(f.get("path","")):
                errors.append(f"{rp}: unsafe file path {f.get('path')!r}")
                continue

            rel = Path(f["path"])
            full = ROOT / rel
            if f.get("name") != rel.name:
                errors.append(f"{rp}: file name does not match path basename for {f['path']}")
            if not isinstance(f.get("fileType"),str) or not f["fileType"]:
                errors.append(f"{rp}: fileType required for {f['path']}")
            if not isinstance(f.get("mediaType"),str) or not f["mediaType"]:
                errors.append(f"{rp}: mediaType required for {f['path']}")
            if not isinstance(f.get("sizeBytes"),int) or f["sizeBytes"] < 0:
                errors.append(f"{rp}: invalid sizeBytes for {f['path']}")
            if not full.is_file():
                errors.append(f"{rp}: broken local file path {f['path']}")
                continue
            if full.stat().st_size != f["sizeBytes"]:
                errors.append(f"{rp}: size mismatch {f['path']} expected={f['sizeBytes']} actual={full.stat().st_size}")

            integ = f.get("integrity")
            if not isinstance(integ,dict):
                errors.append(f"{rp}: integrity must be an object for {f['path']}")
                integ = {}
            blob = integ.get("gitBlobSha1")
            sha = integ.get("sha256")
            if blob is not None and (not isinstance(blob,str) or not SHA1_RE.fullmatch(blob)):
                errors.append(f"{rp}: invalid gitBlobSha1 for {f['path']}")
            if sha is not None and (not isinstance(sha,str) or not SHA256_RE.fullmatch(sha)):
                errors.append(f"{rp}: invalid sha256 for {f['path']}")
            if blob:
                actual_blob = git_blob_sha1(full)
                if actual_blob and actual_blob != blob:
                    errors.append(f"{rp}: git blob mismatch {f['path']}")
            if sha:
                if sha256_file(full) != sha:
                    errors.append(f"{rp}: sha256 mismatch {f['path']}")
            elif r.get("status") == "final" and f.get("relationship") == "owned":
                errors.append(f"{rp}: final owned file missing sha256 {f['path']}")

            if f.get("role") == "redirect" and f.get("relationship") == "referenced" and f.get("mediaType") == "text/html":
                try:
                    redirect_html = full.read_text(encoding="utf-8-sig")
                except UnicodeDecodeError:
                    errors.append(f"{rp}: redirect file is not UTF-8 HTML: {f['path']}")
                else:
                    canonical_url = r.get("canonicalUrl", "")
                    canonical_target = urlparse(canonical_url).path or "/"
                    if canonical_url not in redirect_html and canonical_target not in redirect_html:
                        errors.append(f"{rp}: redirect {f['path']} does not target canonical URL {canonical_url}")

            if f.get("relationship") == "owned":
                p = rel.as_posix()
                owned_paths.add(p)
                previous = globally_owned.get(p)
                if previous and previous != rid:
                    errors.append(f"{rp}: {p} is already owned by {previous}; shared files must be referenced")
                globally_owned[p] = rid
                if f.get("role") == "primary":
                    primary_owned.append(p)

        if not primary_owned:
            errors.append(f"{rp}: at least one owned primary file is required")
        if r.get("canonicalPath") not in primary_owned:
            errors.append(f"{rp}: canonicalPath must be one of the owned primary files")

        if package.get("strict") and package.get("mode") == "directory" and safe_repo_path(package.get("root","")):
            package_root = (ROOT / package["root"]).resolve()
            if not package_root.is_dir():
                errors.append(f"{rp}: strict package root missing: {package['root']}")
            else:
                actual = {p.relative_to(ROOT).as_posix() for p in package_root.rglob("*") if p.is_file()}
                missing_manifest = sorted(actual - owned_paths)
                if missing_manifest:
                    errors.append(f"{rp}: unregistered files inside strict package: {missing_manifest}")
                for p in owned_paths:
                    try:
                        (ROOT / p).resolve().relative_to(package_root)
                    except ValueError:
                        errors.append(f"{rp}: owned file outside strict package: {p}")

    return errors

def summary_record(r):
    return {
        "id": r["id"],
        **({"reportId":r["reportId"]} if r.get("reportId") else {}),
        "recordPath": r["_recordPath"],
        "contentClass": r["contentClass"],
        **({"reportClass":r.get("reportClass")} if r.get("reportClass") else {}),
        **({"publicationClass":r.get("publicationClass")} if r.get("publicationClass") else {}),
        "title": r["title"],
        "status": r["status"],
        "issuedAt": r["issuedAt"],
        **({"period":r.get("period")} if r.get("period") else {}),
        "canonicalPath": r["canonicalPath"],
        "canonicalUrl": r["canonicalUrl"],
        "formats": r["formats"],
        "audience": r["audience"],
        "fileCount": len(r["files"]),
    }

def sort_key(r):
    period = r.get("period") or {}
    return (period.get("end") or (period.get("effectiveAt") or "")[:10] or r.get("issuedAt",""), r.get("issuedAt",""), r["id"])

def build_indexes(records):
    INDEXES.mkdir(parents=True, exist_ok=True)
    ordered = sorted(records, key=sort_key, reverse=True)
    write_json(INDEXES / "all.json", {"schemaVersion":"2.0","count":len(ordered),"records":[summary_record(r) for r in ordered]})
    for cls, filename in INDEX_NAMES.items():
        subset = [summary_record(r) for r in ordered if r["contentClass"] == cls]
        write_json(INDEXES / filename, {"schemaVersion":"2.0","contentClass":cls,"count":len(subset),"records":subset})

    current = {}
    for r in ordered:
        if r["contentClass"] == "report" and r["status"] == "final":
            rc = r.get("reportClass")
            if rc and rc not in current:
                current[rc] = {
                    "id":r["id"],"reportId":r["reportId"],"title":r["title"],
                    "issuedAt":r["issuedAt"],"period":r.get("period"),
                    "canonicalPath":r["canonicalPath"],"canonicalUrl":r["canonicalUrl"]
                }
    write_json(INDEXES / "current.json", {"schemaVersion":"2.0","reports":current})

def generate_catalog(records):
    if not PRESENTATION.is_file():
        return
    cfg = read_json(PRESENTATION)
    by_id = {r["id"]:r for r in records}

    def hydrate(obj):
        if isinstance(obj,list):
            return [hydrate(x) for x in obj]
        if not isinstance(obj,dict):
            return obj
        out = {k:hydrate(v) for k,v in obj.items() if k != "recordId"}
        rid = obj.get("recordId")
        if rid:
            if rid not in by_id:
                raise ValueError(f"presentation references unknown recordId {rid}")
            r = by_id[rid]
            out["href"] = urlparse(r["canonicalUrl"]).path or "/"
            out.setdefault("title", r["title"])
            out.setdefault("summary", r["summary"])
            out["tags"] = " ".join(r.get("tags",[]))
        return out

    write_json(CATALOG_OUT, hydrate(cfg))

def build(records):
    build_indexes(records)
    generate_catalog(records)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("command", choices=["validate","build","check","refresh"])
    args = ap.parse_args()

    if args.command == "refresh":
        changed = refresh_records()
        records = load_records()
        errors = validate(records)
        if errors:
            print("Registry validation FAILED after refresh")
            for e in errors:
                print(" -", e)
            return 1
        build(records)
        print(f"Registry refresh OK: {len(records)} records; {changed} record files updated")
        return 0

    records = load_records()
    if args.command in ("validate","check"):
        errors = validate(records)
        if errors:
            print("Registry validation FAILED")
            for e in errors:
                print(" -", e)
            return 1
        print(f"Registry validation OK: {len(records)} records")

    if args.command in ("build","check"):
        build(records)
        print("Registry indexes and Signal catalog built")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
