#!/usr/bin/env python3
"""Signal Registry v2 validator, manifest refresher, index builder, and catalog generator."""

from __future__ import annotations

import argparse
import hashlib
import json
import mimetypes
import re
import subprocess
from datetime import date, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "registry"
RECORDS = REGISTRY / "records"
INDEXES = REGISTRY / "indexes"
PRESENTATION = REGISTRY / "presentation" / "signals-catalog.json"
CATALOG_OUT = ROOT / "js" / "signals-catalog.json"

REQUIRED = {"schemaVersion","id","contentClass","title","status","audience","formats","issuedAt","canonicalPath","package","files"}
CLASSES = {"report","publication","dispatch","media"}
STATUSES = {"draft","review","final","superseded","withdrawn"}
RELATIONSHIPS = {"owned","referenced"}
REPORT_CLASSES = {"eod","eow","mtd","eom","quarterly","annual","milestone","incident","audit","compliance","release-readiness","production-validation","investigation","risk-review","special"}
AUDIENCES = {"internal","executive","operations","staff","stakeholder","shareholder","advisor","partner","public","client","community"}
ROLES = {"primary","report-section","audio","video","image","transcript","source","data","metadata","style","script","readme","redirect","evidence","attachment","other"}
ID_RE = re.compile(r"^AV-[A-Z]+-[A-Z0-9-]+$")

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
    if ext in {".css"}:
        return "style"
    if ext in {".js",".mjs",".ps1",".py"}:
        return "script"
    if "transcript" in p or "bytecast" in p:
        return "transcript"
    if "/reports/" in p and ext in {".html",".md"}:
        return "report-section"
    if "/sources/" in p or "appendix" in name or ext == ".md":
        return "source"
    if ext in {".json",".csv"}:
        return "data"
    if ext in {".pdf",".docx",".xlsx",".pptx"}:
        return "attachment"
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
    if package.get("mode") != "directory" or not root_rel:
        return None
    package_root = ROOT / root_rel
    if not package_root.is_dir():
        return None

    existing_refs = [f for f in record.get("files", []) if f.get("relationship") == "referenced"]
    owned = []
    for full in sorted(p for p in package_root.rglob("*") if p.is_file()):
        rel = full.relative_to(ROOT).as_posix()
        local = full.relative_to(package_root)
        role = infer_role(local)
        owned.append(enrich_file_entry({
            "id": stable_file_id(local.as_posix()),
            "role": role,
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
    period = record.get("period")
    if record.get("contentClass") != "report":
        return
    if not isinstance(period, dict) or not period:
        errors.append(f"{rp}: period required for reports")
        return
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
            if start and end and start > end:
                errors.append(f"{rp}: period.start must be <= period.end")
            issued = parse_date(record.get("issuedAt",""), "issuedAt", errors, rp)
            if issued and end and issued < end:
                errors.append(f"{rp}: issuedAt cannot be before period.end")
    if has_effective:
        try:
            datetime.fromisoformat(period["effectiveAt"].replace("Z","+00:00"))
        except Exception:
            errors.append(f"{rp}: period.effectiveAt must be ISO-8601 date-time")

def validate(records):
    errors = []
    ids = set()

    for r in records:
        rp = r["_recordPath"]
        missing = REQUIRED - set(r)
        if missing:
            errors.append(f"{rp}: missing required fields: {sorted(missing)}")
            continue

        if r["schemaVersion"] != "2.0":
            errors.append(f"{rp}: schemaVersion must be 2.0")
        if not ID_RE.fullmatch(r["id"]):
            errors.append(f"{rp}: invalid id format {r['id']}")
        if r["id"] in ids:
            errors.append(f"{rp}: duplicate id {r['id']}")
        ids.add(r["id"])

        if r["contentClass"] not in CLASSES:
            errors.append(f"{rp}: invalid contentClass {r['contentClass']}")
        if r["status"] not in STATUSES:
            errors.append(f"{rp}: invalid status {r['status']}")
        if not isinstance(r["audience"], list) or not r["audience"]:
            errors.append(f"{rp}: audience must be a non-empty array")
        else:
            unknown = sorted(set(r["audience"]) - AUDIENCES)
            if unknown:
                errors.append(f"{rp}: invalid audience values {unknown}")
            if len(r["audience"]) != len(set(r["audience"])):
                errors.append(f"{rp}: audience contains duplicates")
        if not isinstance(r["formats"], list) or not r["formats"]:
            errors.append(f"{rp}: formats must be a non-empty array")
        elif len(r["formats"]) != len(set(r["formats"])):
            errors.append(f"{rp}: formats contains duplicates")

        issued = parse_date(r["issuedAt"], "issuedAt", errors, rp)

        if r["contentClass"] == "report":
            if r.get("reportId") != r["id"]:
                errors.append(f"{rp}: reportId must equal id")
            if r.get("reportClass") not in REPORT_CLASSES:
                errors.append(f"{rp}: invalid or missing reportClass")
            if r["status"] == "final" and not r.get("canonicalUrl"):
                errors.append(f"{rp}: final report requires canonicalUrl")
        validate_period(r, rp, errors)

        canonical = ROOT / r["canonicalPath"]
        if not canonical.is_file():
            errors.append(f"{rp}: canonicalPath does not exist: {r['canonicalPath']}")

        package = r["package"]
        if package.get("mode") not in {"directory","legacy-flat","external"}:
            errors.append(f"{rp}: invalid package.mode")
        if not isinstance(package.get("strict"), bool):
            errors.append(f"{rp}: package.strict must be boolean")

        files = r["files"]
        if not isinstance(files, list) or not files:
            errors.append(f"{rp}: files must be a non-empty array")
            continue

        file_ids = set()
        owned_paths = set()
        primary_owned = []
        for f in files:
            req = {"id","role","relationship","path","name","fileType","mediaType"}
            fm = req - set(f)
            if fm:
                errors.append(f"{rp}: file entry missing {sorted(fm)}")
                continue
            if f["id"] in file_ids:
                errors.append(f"{rp}: duplicate file id {f['id']}")
            file_ids.add(f["id"])
            if f["role"] not in ROLES:
                errors.append(f"{rp}: invalid file role {f['role']} for {f['path']}")
            if f["relationship"] not in RELATIONSHIPS:
                errors.append(f"{rp}: invalid relationship for {f['path']}")
                continue

            rel = Path(f["path"])
            if rel.is_absolute() or ".." in rel.parts:
                errors.append(f"{rp}: unsafe file path {f['path']}")
                continue
            full = ROOT / rel
            if not full.is_file():
                errors.append(f"{rp}: broken local file path {f['path']}")
                continue

            if "sizeBytes" in f and full.stat().st_size != f["sizeBytes"]:
                errors.append(f"{rp}: size mismatch {f['path']} expected={f['sizeBytes']} actual={full.stat().st_size}")

            integ = f.get("integrity") or {}
            expected_blob = integ.get("gitBlobSha1")
            if expected_blob:
                actual_blob = git_blob_sha1(full)
                if actual_blob and actual_blob != expected_blob:
                    errors.append(f"{rp}: git blob mismatch {f['path']}")
            expected_sha = integ.get("sha256")
            if expected_sha:
                actual_sha = sha256_file(full)
                if actual_sha != expected_sha:
                    errors.append(f"{rp}: sha256 mismatch {f['path']}")
            elif r["status"] == "final" and f["relationship"] == "owned":
                errors.append(f"{rp}: final owned file missing sha256 {f['path']}")

            if f["relationship"] == "owned":
                owned_paths.add(rel.as_posix())
                if f["role"] == "primary":
                    primary_owned.append(rel.as_posix())

        if not primary_owned:
            errors.append(f"{rp}: at least one owned primary file is required")
        if r["canonicalPath"] not in primary_owned:
            errors.append(f"{rp}: canonicalPath must be one of the owned primary files")

        if package.get("strict") and package.get("mode") == "directory":
            package_root = ROOT / package["root"]
            if not package_root.is_dir():
                errors.append(f"{rp}: strict package root missing: {package['root']}")
            else:
                actual = {p.relative_to(ROOT).as_posix() for p in package_root.rglob("*") if p.is_file()}
                missing_manifest = sorted(actual - owned_paths)
                outside_package = sorted(p for p in owned_paths if not (ROOT / p).is_relative_to(package_root))
                if missing_manifest:
                    errors.append(f"{rp}: unregistered files inside strict package: {missing_manifest}")
                if outside_package:
                    errors.append(f"{rp}: owned files outside strict package: {outside_package}")

    return errors

def summary_record(r):
    period = r.get("period")
    return {
        "id": r["id"],
        "recordPath": r["_recordPath"],
        "contentClass": r["contentClass"],
        **({"reportClass": r.get("reportClass")} if r["contentClass"] == "report" else {}),
        **({"publicationClass": r.get("publicationClass")} if r.get("publicationClass") else {}),
        "title": r["title"],
        "status": r["status"],
        "issuedAt": r["issuedAt"],
        **({"period": period} if period else {}),
        "canonicalPath": r["canonicalPath"],
        **({"canonicalUrl": r.get("canonicalUrl")} if r.get("canonicalUrl") else {}),
        "formats": r["formats"],
        "audience": r["audience"],
        "fileCount": len(r["files"]),
    }

def sort_key(r):
    period = r.get("period") or {}
    return (period.get("end") or period.get("effectiveAt") or r.get("issuedAt",""), r.get("issuedAt",""), r["id"])

def build_indexes(records):
    INDEXES.mkdir(parents=True, exist_ok=True)
    ordered = sorted(records, key=sort_key, reverse=True)
    summaries = [summary_record(r) for r in ordered]
    write_json(INDEXES / "all.json", {"schemaVersion":"2.0","count":len(summaries),"records":summaries})

    for cls, filename in INDEX_NAMES.items():
        subset = [summary_record(r) for r in ordered if r["contentClass"] == cls]
        write_json(INDEXES / filename, {"schemaVersion":"2.0","contentClass":cls,"count":len(subset),"records":subset})

    current = {}
    finals = [r for r in ordered if r["contentClass"] == "report" and r["status"] == "final"]
    for r in finals:
        rc = r.get("reportClass")
        if rc and rc not in current:
            current[rc] = {
                "id": r["id"],
                "title": r["title"],
                "issuedAt": r["issuedAt"],
                "period": r.get("period"),
                "canonicalPath": r["canonicalPath"],
                "canonicalUrl": r.get("canonicalUrl"),
            }
    write_json(INDEXES / "current.json", {"schemaVersion":"2.0","reports":current})

def generate_catalog(records):
    if not PRESENTATION.is_file():
        return
    cfg = read_json(PRESENTATION)
    known = {r["id"] for r in records}

    def scrub(obj):
        if isinstance(obj, list):
            return [scrub(x) for x in obj]
        if isinstance(obj, dict):
            rid = obj.get("recordId")
            if rid and rid not in known:
                raise ValueError(f"presentation references unknown recordId {rid}")
            return {k:scrub(v) for k,v in obj.items() if k != "recordId"}
        return obj

    write_json(CATALOG_OUT, scrub(cfg))

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
