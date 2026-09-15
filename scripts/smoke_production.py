#!/usr/bin/env python3
"""Verify that the deployed Signal matches the repository's governed catalog."""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_CATALOG = ROOT / "js" / "signals-catalog.json"
USER_AGENT = "AeroVista-Signal-Smoke/1.0"


def fetch_text(url, timeout=20):
    request = Request(url, headers={"User-Agent": USER_AGENT, "Accept": "*/*"})
    with urlopen(request, timeout=timeout) as response:
        status = getattr(response, "status", 200)
        if status != 200:
            raise AssertionError(f"{url} returned HTTP {status}")
        return response.read().decode("utf-8")


def fetch_json(url):
    return json.loads(fetch_text(url))


def current_report(index):
    reports = list(index.get("reports", {}).values())
    if not reports:
        raise AssertionError("production current report index is empty")

    def key(record):
        period = record.get("period") or {}
        effective = (period.get("effectiveAt") or "")[:10]
        return (
            period.get("end") or effective or record.get("issuedAt", ""),
            record.get("issuedAt", ""),
            record.get("id", ""),
        )

    return max(reports, key=key)


def check_production(base_url):
    base_url = base_url.rstrip("/") + "/"
    expected = json.loads(EXPECTED_CATALOG.read_text(encoding="utf-8"))
    deployed = fetch_json(urljoin(base_url, "js/signals-catalog.json"))

    for field in ("updated",):
        if deployed.get(field) != expected.get(field):
            raise AssertionError(
                f"deployed catalog {field}={deployed.get(field)!r}; expected {expected.get(field)!r}"
            )
    for field in ("label", "title", "summary", "href", "stats", "tags"):
        actual = deployed.get("featured", {}).get(field)
        wanted = expected.get("featured", {}).get(field)
        if actual != wanted:
            raise AssertionError(f"deployed featured.{field}={actual!r}; expected {wanted!r}")

    home = fetch_text(base_url)
    if "render-signals-hub.js" not in home:
        raise AssertionError("homepage is not loading the governed Signal hub renderer")

    featured = deployed["featured"]
    featured_url = urljoin(base_url, featured["href"].lstrip("/"))
    report_html = fetch_text(featured_url)
    if featured["title"] not in report_html:
        raise AssertionError("featured report title is missing from the deployed report page")
    canonical_path = urlparse(featured_url).path
    if featured_url not in report_html and canonical_path not in report_html:
        raise AssertionError("featured report page does not declare its canonical publication path")

    index = fetch_json(urljoin(base_url, "registry/indexes/current.json"))
    latest = current_report(index)
    if urlparse(latest["canonicalUrl"]).path != featured["href"]:
        raise AssertionError(
            "featured report is not the newest final report in the deployed current index"
        )

    return {
        "baseUrl": base_url,
        "featured": featured["title"],
        "featuredUrl": featured_url,
        "currentReportId": latest["id"],
        "catalogUpdated": deployed["updated"],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--base-url",
        default="https://thesignal.aerovista.us/",
        help="Production origin to verify",
    )
    parser.add_argument("--attempts", type=int, default=12)
    parser.add_argument("--delay", type=int, default=10)
    args = parser.parse_args()

    last_error = None
    for attempt in range(1, args.attempts + 1):
        try:
            result = check_production(args.base_url)
            print(json.dumps({"ok": True, **result}, indent=2))
            return 0
        except Exception as exc:
            last_error = exc
            print(f"Attempt {attempt}/{args.attempts} failed: {exc}", file=sys.stderr)
            if attempt < args.attempts:
                time.sleep(args.delay)

    print(f"Production smoke gate FAILED: {last_error}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
