#!/usr/bin/env python3
"""Signal Registry v2 validator and index builder. Standard library only."""

from __future__ import annotations
import argparse
import hashlib
import json
import mimetypes
import subprocess
import sys
from pathlib import Path
from datetime import date

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "registry"
RECORDS = REGISTRY / "records"
INDEXES = REGISTRY / "indexes"

REQUIRED = {"schemaVersion","id","contentClass","title","status","audience","formats","issuedAt","package","files"}
CLASSES = {"report","publication","dispatch","media"}
STATUSES = {"draft","review","final","superseded","withdrawn"}
RELATIONSHIPS = {"owned","referenced"}

def load_records():
    records = []
    for path in sorted(RECORDS.glob("*/*.json")):
        with path.open(encoding="utf-8") as f:
            obj = json.load(f)
        obj["_recordPath"] = path.relative_to(ROOT).as_posix()
        records.append(obj)
    return records

def git_blob_sha1(path: Path):
    try:
        cp = subprocess.run(["git","hash-object",str(path)], cwd=ROOT, text=True, capture_output=True, check=True)
        return cp.stdout.strip()
    except Exception:
        return None

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
        if r["id"] in ids:
            errors.append(f"{rp}: duplicate id {r['id']}")
        ids.add(r["id"])
        if r["contentClass"] not in CLASSES:
            errors.append(f"{rp}: invalid contentClass {r['contentClass']}")
        if r["status"] not in STATUSES:
            errors.append(f"{rp}: invalid status {r['status']}")
        if r["contentClass"] == "report":
            if not r.get("reportClass"):
                errors.append(f"{rp}: reportClass required for reports")
            if not r.get("period"):
                errors.append(f"{rp}: period required for reports")
        try:
            date.fromisoformat(r["issuedAt"])
        except Exception:
            errors.append(f"{rp}: issuedAt must be YYYY-MM-DD")

        file_ids = set()
        owned_paths = set()
        for f in r["files"]:
            for key in ("id","role","relationship","path","name","mediaType"):
                if key not in f:
                    errors.append(f"{rp}: file entry missing {key}")
                    continue
            if f.get("id") in file_ids:
                errors.append(f"{rp}: duplicate file id {f.get('id')}")
            file_ids.add(f.get("id"))
            if f.get("relationship") not in RELATIONSHIPS:
                errors.append(f"{rp}: invalid relationship for {f.get('path')}")
                continue
            if f.get("relationship") != "owned":
                continue

            rel = Path(f["path"])
            owned_paths.add(rel.as_posix())
            full = ROOT / rel
            if not full.is_file():
                errors.append(f"{rp}: missing owned file {rel.as_posix()}")
                continue
            if "sizeBytes" in f and full.stat().st_size != f["sizeBytes"]:
                errors.append(f"{rp}: size mismatch {rel.as_posix()} expected={f['sizeBytes']} actual={full.stat().st_size}")
            expected = (f.get("integrity") or {}).get("gitBlobSha1")
            if expected:
                actual = git_blob_sha1(full)
                if actual and actual != expected:
                    errors.append(f"{rp}: git blob mismatch {rel.as_posix()} expected={expected} actual={actual}")

        package = r["package"]
        if package.get("strict") and package.get("mode") == "directory":
            package_root = ROOT / package["root"]
            if not package_root.is_dir():
                errors.append(f"{rp}: strict package root missing: {package['root']}")
            else:
                actual = {
                    p.relative_to(ROOT).as_posix()
                    for p in package_root.rglob("*")
                    if p.is_file()
                }
                missing_manifest = sorted(actual - owned_paths)
                outside_package = sorted(
                    p for p in owned_paths
                    if not (ROOT / p).is_relative_to(package_root)
                )
                if missing_manifest:
                    errors.append(f"{rp}: unregistered files inside strict package: {missing_manifest}")
                if outside_package:
                    errors.append(f"{rp}: owned files outside strict package: {outside_package}")
    return errors

def clean_record(r):
    return {k:v for k,v in r.items() if not k.startswith("_")}

def sort_key(r):
    period = r.get("period") or {}
    return (period.get("end") or period.get("effectiveAt") or r.get("issuedAt",""), r.get("issuedAt",""), r["id"])

def build(records):
    INDEXES.mkdir(parents=True, exist_ok=True)
    clean = [clean_record(r) for r in records]
    clean.sort(key=sort_key, reverse=True)

    def write(name, payload):
        (INDEXES / name).write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    write("all.json", {"schemaVersion":"2.0","count":len(clean),"records":clean})
    for cls in sorted(CLASSES):
        subset = [r for r in clean if r["contentClass"] == cls]
        write(f"{cls}s.json", {"schemaVersion":"2.0","contentClass":cls,"count":len(subset),"records":subset})

    current = {}
    finals = [r for r in clean if r["contentClass"] == "report" and r["status"] == "final"]
    for r in finals:
        rc = r.get("reportClass")
        if rc and rc not in current:
            current[rc] = {
                "id": r["id"],
                "title": r["title"],
                "issuedAt": r["issuedAt"],
                "period": r.get("period"),
                "canonicalUrl": r.get("canonicalUrl")
            }
    write("current.json", {"schemaVersion":"2.0","reports":current})

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("command", choices=["validate","build","check"])
    args = ap.parse_args()
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
        print("Registry indexes built")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
