#!/usr/bin/env python3
"""Regression tests for the production smoke gate."""

from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path
from unittest import mock

SCRIPT = Path(__file__).with_name("smoke_production.py")
spec = importlib.util.spec_from_file_location("smoke_production", SCRIPT)
smoke = importlib.util.module_from_spec(spec)
spec.loader.exec_module(smoke)


class ProductionSmokeTests(unittest.TestCase):
    def setUp(self):
        self.featured = {
            "label": "Latest EOD",
            "title": "Current Report",
            "summary": "Current governed report.",
            "href": "/reports/current/",
            "stats": [{"value": "Sep 13", "label": "Issued"}],
            "tags": "current report",
        }
        self.catalog = {"updated": "2026-09-13", "featured": self.featured}
        self.index = {
            "reports": {
                "eow": {
                    "id": "AV-RPT-EOW-2026-09-07",
                    "issuedAt": "2026-09-08",
                    "period": {"start": "2026-09-01", "end": "2026-09-07"},
                    "canonicalUrl": "https://example.test/reports/weekly/",
                },
                "eod": {
                    "id": "AV-RPT-EOD-2026-09-13",
                    "issuedAt": "2026-09-13",
                    "period": {"start": "2026-09-11", "end": "2026-09-13"},
                    "canonicalUrl": "https://example.test/reports/current/",
                },
            }
        }

    def test_current_report_selects_latest_period(self):
        self.assertEqual(
            smoke.current_report(self.index)["id"], "AV-RPT-EOD-2026-09-13"
        )

    def test_check_production_accepts_matching_deployment(self):
        expected_file = mock.Mock()
        expected_file.read_text.return_value = json.dumps(self.catalog)

        def json_response(url):
            return self.catalog if url.endswith("signals-catalog.json") else self.index

        def text_response(url, timeout=20):
            if url == "https://example.test/":
                return '<script src="/js/render-signals-hub.js"></script>'
            return '<link rel="canonical" href="https://example.test/reports/current/">Current Report'

        with (
            mock.patch.object(smoke, "EXPECTED_CATALOG", expected_file),
            mock.patch.object(smoke, "fetch_json", side_effect=json_response),
            mock.patch.object(smoke, "fetch_text", side_effect=text_response),
        ):
            result = smoke.check_production("https://example.test/")

        self.assertEqual(result["currentReportId"], "AV-RPT-EOD-2026-09-13")

    def test_check_production_rejects_stale_feature(self):
        expected_file = mock.Mock()
        expected_file.read_text.return_value = json.dumps(self.catalog)
        stale = json.loads(json.dumps(self.catalog))
        stale["featured"]["title"] = "Old Report"

        with (
            mock.patch.object(smoke, "EXPECTED_CATALOG", expected_file),
            mock.patch.object(smoke, "fetch_json", return_value=stale),
        ):
            with self.assertRaisesRegex(AssertionError, "featured.title"):
                smoke.check_production("https://example.test/")


if __name__ == "__main__":
    unittest.main()
