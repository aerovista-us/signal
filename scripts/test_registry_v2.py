#!/usr/bin/env python3
"""Regression tests for Signal Registry v2 semantic validation."""

from __future__ import annotations

import copy
import importlib.util
import unittest
from pathlib import Path

SCRIPT = Path(__file__).with_name("registry_v2.py")
spec = importlib.util.spec_from_file_location("registry_v2", SCRIPT)
registry = importlib.util.module_from_spec(spec)
spec.loader.exec_module(registry)


class RegistryV2ValidationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.records = registry.load_records()
        cls.small_report = next(r for r in cls.records if r["id"] == "AV-RPT-EOW-2026-05-23")

    def test_current_registry_is_valid(self):
        self.assertEqual(registry.validate(self.records), [])

    def test_duplicate_ids_fail(self):
        a = copy.deepcopy(self.small_report)
        b = copy.deepcopy(self.small_report)
        errors = registry.validate([a, b])
        self.assertTrue(any("duplicate id" in e for e in errors), errors)

    def test_invalid_period_order_fails(self):
        record = copy.deepcopy(self.small_report)
        record["period"] = {"start": "2026-05-24", "end": "2026-05-23"}
        errors = registry.validate([record])
        self.assertTrue(any("period.start must be <= period.end" in e for e in errors), errors)

    def test_final_owned_file_requires_sha256(self):
        record = copy.deepcopy(self.small_report)
        record["files"][0]["integrity"].pop("sha256", None)
        errors = registry.validate([record])
        self.assertTrue(any("missing sha256" in e for e in errors), errors)

    def test_unsafe_file_path_fails(self):
        record = copy.deepcopy(self.small_report)
        record["files"][0]["path"] = "../outside.html"
        errors = registry.validate([record])
        self.assertTrue(any("unsafe file path" in e for e in errors), errors)

    def test_invalid_report_class_and_audience_fail(self):
        record = copy.deepcopy(self.small_report)
        record["reportClass"] = "weekly-ish"
        record["audience"] = ["internal", "mystery"]
        errors = registry.validate([record])
        self.assertTrue(any("invalid or missing reportClass" in e for e in errors), errors)
        self.assertTrue(any("invalid audience" in e for e in errors), errors)

    def test_registered_html_redirects_target_canonical_url(self):
        checked = 0
        for record in self.records:
            canonical_url = record.get("canonicalUrl", "")
            canonical_target = registry.urlparse(canonical_url).path or "/"
            for asset in record.get("files", []):
                if asset.get("role") != "redirect" or asset.get("mediaType") != "text/html":
                    continue
                html = (registry.ROOT / asset["path"]).read_text(encoding="utf-8-sig")
                self.assertTrue(
                    canonical_url in html or canonical_target in html,
                    f"{record['id']} redirect {asset['path']} does not target {canonical_url}",
                )
                checked += 1
        self.assertGreater(checked, 0, "expected at least one registered HTML redirect")

    def test_featured_selection_uses_latest_final_report(self):
        featured = registry.select_featured_record(
            self.records, {"mode": "latest-final-report"}
        )
        self.assertEqual(featured["id"], "AV-RPT-EOD-2026-09-13")

    def test_featured_selection_can_filter_report_classes(self):
        featured = registry.select_featured_record(
            self.records,
            {"mode": "latest-final-report", "reportClasses": ["eow"]},
        )
        self.assertEqual(featured["id"], "AV-RPT-EOW-2026-09-07")

    def test_automatic_featured_uses_canonical_registry_metadata(self):
        featured, record = registry.automatic_featured(
            self.records, {"mode": "latest-final-report"}
        )
        self.assertEqual(featured["title"], record["title"])
        self.assertEqual(featured["summary"], record["summary"])
        self.assertEqual(featured["href"], "/newsletters/editions/eod/2026-09-13-48-hour-shareholder-partner-update/")
        self.assertEqual(featured["stats"][0]["value"], "Sep 11–13")


if __name__ == "__main__":
    unittest.main()
