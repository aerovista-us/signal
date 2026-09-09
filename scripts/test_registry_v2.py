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


if __name__ == "__main__":
    unittest.main()
