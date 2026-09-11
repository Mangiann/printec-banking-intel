"""Tests for the (country, workstream) resolver (scripts/scout_config.py) behind /printec-market-research.

Any country works; the research is one of the fixed workstreams (A1-A6, A8); storage is PER COUNTRY (one
registry + one Excel per country, workstream-tagged). Run: python tests/test_scout_config.py
"""
import os
import sys
import tempfile
import unittest
from pathlib import Path

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "scripts"))
sys.path.insert(0, os.path.join(ROOT, "review"))

import scout_config as sc  # noqa: E402


class ResolveCountry(unittest.TestCase):
    def test_known_and_substring(self):
        self.assertEqual(sc.resolve_country(country="Greece")[0], "GR")
        self.assertEqual(sc.resolve_country(country="tenders in romania")[0], "RO")

    def test_any_country_via_explicit_iso_langs(self):
        self.assertEqual(sc.resolve_country(iso="FR", name="France", languages=["fr"]),
                         ("FR", "France", ["fr"]))                       # not in the map -> still works

    def test_austria_not_excluded(self):
        self.assertEqual(sc.resolve_country(country="Austria")[0], "AT")

    def test_unknown_is_none(self):
        self.assertIsNone(sc.resolve_country(country="Narnia"))


class Build(unittest.TestCase):
    def _b(self, **kw):
        tmp = tempfile.mkdtemp()
        kw.setdefault("data_root", os.path.join(tmp, "data"))
        kw.setdefault("configs_dir", os.path.join(tmp, "cfg"))
        return sc.build(**kw)

    def test_workstream_drives_topics_and_run_id(self):
        out = self._b(country="Greece", workstream="A2")
        self.assertEqual(out["workstream"], "A2")
        self.assertIn("tenders", out["topics"])                          # A2's canonical topics
        self.assertEqual(out["languages"], ["el", "en"])
        self.assertTrue(out["run_id"].startswith("dr_gr_a2_live_"))
        self.assertEqual(out["deliverable_name"], "Greece - Banking & Payments Sources.xlsx")

    def test_storage_is_per_country_across_workstreams(self):
        tmp = tempfile.mkdtemp()                                        # SAME data-root for both builds
        dr, cf = os.path.join(tmp, "data"), os.path.join(tmp, "cfg")
        a2 = sc.build(country="Greece", workstream="A2", data_root=dr, configs_dir=cf)
        a5 = sc.build(country="Greece", workstream="A5", data_root=dr, configs_dir=cf)
        self.assertTrue(a2["promotion_db"].endswith(os.path.join("registries", "GR.db")))
        self.assertEqual(a2["promotion_db"], a5["promotion_db"])         # SAME country DB
        self.assertEqual(a2["deliverable_name"], a5["deliverable_name"]) # SAME country Excel
        self.assertNotEqual(a2["run_id"], a5["run_id"])                  # distinct runs
        self.assertNotEqual(a2["topics"], a5["topics"])                  # A2 tenders vs A5 jobs

    def test_any_country_builds(self):
        out = self._b(iso="FR", country_name="France", languages=["fr"], workstream="A8")
        self.assertEqual(out["languages"], ["fr", "en"])
        self.assertTrue(out["promotion_db"].endswith(os.path.join("registries", "FR.db")))
        self.assertEqual(out["deliverable_name"], "France - Banking & Payments Sources.xlsx")

    def test_region_scope_own_db_and_zz_records(self):
        out = self._b(iso="EU", languages=["en"], workstream="A8")
        self.assertTrue(out["promotion_db"].endswith(os.path.join("registries", "EU.db")))
        self.assertEqual(out["deliverable_name"], "Europe - Banking & Payments Sources.xlsx")
        self.assertIn("country: ZZ", Path(out["config_path"]).read_text(encoding="utf-8"))   # region -> records ZZ

    def test_us_scope_is_a_real_country(self):
        out = self._b(iso="US", languages=["en"], workstream="A8")
        self.assertTrue(out["promotion_db"].endswith(os.path.join("registries", "US.db")))
        self.assertIn("country: US", Path(out["config_path"]).read_text(encoding="utf-8"))    # US is a real ISO country

    def test_unknown_workstream_rejected(self):
        with self.assertRaises(SystemExit):
            self._b(country="Greece", workstream="A99")

    def test_explicit_run_id_is_reused_not_minted(self):
        out = self._b(country="Greece", workstream="A2", run_id="dr_gr_a2_live_042")   # resume path
        self.assertEqual(out["run_id"], "dr_gr_a2_live_042")

    def test_run_id_increments_within_country_workstream(self):
        tmp = tempfile.mkdtemp()
        d = Path(tmp) / "data" / "source_candidates"
        d.mkdir(parents=True)
        (d / "dr_gr_a2_live_004.jsonl").write_text("{}\n", encoding="utf-8")
        out = sc.build(country="Greece", workstream="A2",
                       data_root=str(Path(tmp) / "data"), configs_dir=os.path.join(tmp, "cfg"))
        self.assertEqual(out["run_id"], "dr_gr_a2_live_005")


if __name__ == "__main__":
    unittest.main()
