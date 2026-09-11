"""The campaign ownership fence (scripts/campaign.py) — two machines share ONE plan without colliding.

Each machine owns the scopes named in `data/campaign_assignment.json`. The driver must never hand out, nor
tick off, a scope it does not own, and a missing/empty/typo'd assignment must STOP rather than quietly fall
back to "run everything" (CLAUDE.md rule 2: a stage that cannot run stops the pipeline; rule 7: a silent
bound may not exist). Run: python tests/test_campaign_assignment.py
"""
import io
import json
import os
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "scripts"))
sys.path.insert(0, os.path.join(ROOT, "review"))

import campaign  # noqa: E402

# A miniature plan: three scopes belonging to two different machines, in plan order.
PLAN_TEXT = """sets:
  - {scope: CZ, workstream: A1, status: pending, runs: 0}
  - {scope: CZ, workstream: A2, status: pending, runs: 0}
  - {scope: HU, workstream: A1, status: pending, runs: 0}
  - {scope: RO, workstream: A1, status: pending, runs: 0}
  - {scope: RO, workstream: A2, status: pending, runs: 0}
"""


class FenceCase(unittest.TestCase):
    """Redirects the driver's plan/state/assignment/priority files into a temp dir, and stubs the descriptor
    so the test exercises the FENCE and never generates real run configs."""

    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self._saved = (campaign.PLAN, campaign.STATE, campaign.ASSIGNMENT, campaign._PRIORITY,
                       campaign._descriptor)
        campaign.PLAN = Path(self.tmp) / "research_plan.yaml"
        campaign.PLAN.write_text(PLAN_TEXT, encoding="utf-8")
        campaign.STATE = Path(self.tmp) / "campaign_state.json"
        campaign.ASSIGNMENT = Path(self.tmp) / "campaign_assignment.json"
        campaign._PRIORITY = Path(self.tmp) / "campaign_priority.json"
        campaign._descriptor = lambda s, w, run_id=None: {
            "scope": s, "workstream": w, "run_id": run_id or f"dr_{s.lower()}_{w.lower()}_live_001"}

    def tearDown(self):
        (campaign.PLAN, campaign.STATE, campaign.ASSIGNMENT, campaign._PRIORITY,
         campaign._descriptor) = self._saved

    def assign(self, owner, scopes):
        campaign.ASSIGNMENT.write_text(json.dumps({"owner": owner, "scopes": scopes}), encoding="utf-8")

    def run_ok(self, argv):
        """Run the driver, expecting success; returns the parsed JSON it printed."""
        buf = io.StringIO()
        with redirect_stdout(buf):
            self.assertEqual(campaign.main(argv), 0)
        return json.loads(buf.getvalue())

    def run_refused(self, argv):
        """Run the driver, expecting a LOUD refusal: non-zero exit AND an `error` on stdout."""
        buf = io.StringIO()
        with redirect_stdout(buf):
            with self.assertRaises(SystemExit) as cm:
                campaign.main(argv)
        self.assertNotEqual(cm.exception.code, 0, "a refusal must exit non-zero, not look like success")
        payload = json.loads(buf.getvalue())
        self.assertIn("error", payload)
        return payload


class MissingOrBrokenAssignmentStops(FenceCase):
    def test_no_file_hands_out_nothing(self):
        self.run_refused(["--next"])                     # must NOT fall back to running the whole plan
        self.assertFalse(campaign.STATE.exists(), "a refused --next must not claim a set")

    def test_empty_scopes_stops(self):
        self.assign("nobody", [])
        self.run_refused(["--next"])

    def test_unknown_scope_is_a_typo_not_a_no_op(self):
        self.assign("someone", ["CZ", "CZE"])            # CZE is not in the plan
        out = self.run_refused(["--next"])
        self.assertEqual(out["unknown_scopes"], ["CZE"])

    def test_status_also_stops(self):
        self.run_refused(["--status"])


class HandsOutOnlyOwnedScopes(FenceCase):
    def test_next_skips_another_machines_scope(self):
        self.assign("friend", ["HU"])                    # CZ comes first in plan order, but is not ours
        self.assertEqual(self.run_ok(["--next"])["scope"], "HU")

    def test_two_machines_never_get_the_same_set(self):
        """The guarantee the split rests on: disjoint assignments => disjoint work, whatever the plan order."""
        mine, theirs = ["CZ", "HU"], ["RO"]
        seen_a, seen_b = set(), set()
        for scopes, seen in ((mine, seen_a), (theirs, seen_b)):
            campaign.STATE.unlink(missing_ok=True)
            self.assign("m", scopes)
            while True:
                out = self.run_ok(["--next"])
                if out.get("done_all"):
                    break
                seen.add((out["scope"], out["workstream"]))
                self.run_ok(["--complete", out["scope"], out["workstream"]])
        self.assertEqual(seen_a, {("CZ", "A1"), ("CZ", "A2"), ("HU", "A1")})
        self.assertEqual(seen_b, {("RO", "A1"), ("RO", "A2")})
        self.assertEqual(seen_a & seen_b, set(), "the two machines overlapped — the fence leaked")

    def test_priority_cannot_jump_into_another_machines_scope(self):
        self.assign("friend", ["HU"])
        campaign._PRIORITY.write_text(json.dumps({"priority": [["RO", "A1"]]}), encoding="utf-8")
        self.assertEqual(self.run_ok(["--next"])["scope"], "HU")   # RO is not ours, so it is ignored

    def test_stale_in_progress_for_an_unowned_scope_is_not_resumed(self):
        self.assign("friend", ["HU"])
        campaign.STATE.write_text(json.dumps(
            {"done": [], "in_progress": {"scope": "RO", "workstream": "A1", "run_id": "x"}}), encoding="utf-8")
        out = self.run_ok(["--next"])
        self.assertEqual(out["scope"], "HU")
        self.assertNotIn("resumed", out)


class CompleteIsFenced(FenceCase):
    def test_refuses_to_tick_off_an_unowned_scope(self):
        self.assign("friend", ["HU"])
        self.run_refused(["--complete", "RO", "A1"])
        self.assertFalse(campaign.STATE.exists(), "a refused --complete must not write state")

    def test_accepts_an_owned_scope_and_counts_only_ours(self):
        self.assign("friend", ["CZ", "HU"])
        out = self.run_ok(["--complete", "cz", "A1"])   # lower case is normalised
        self.assertEqual(out["completed"], ["CZ", "A1"])
        self.assertEqual((out["done"], out["total"], out["remaining"]), (1, 3, 2))   # 3 = CZ*2 + HU*1, not 5


class StatusReportsOurShare(FenceCase):
    def test_counts_and_lists_only_our_sets(self):
        self.assign("friend", ["CZ", "HU"])
        self.run_ok(["--complete", "CZ", "A1"])
        out = self.run_ok(["--status"])
        self.assertEqual((out["done"], out["total"], out["remaining"]), (1, 3, 2))
        self.assertEqual(out["remaining_sets"], ["CZ/A2", "HU/A1"])
        self.assertEqual(out["plan_total_all_machines"], 5)         # the whole plan is still reported, honestly
        self.assertEqual(out["scopes"], ["CZ", "HU"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
