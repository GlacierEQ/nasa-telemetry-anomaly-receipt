import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE = json.loads((ROOT / "machine" / "excellence-state.json").read_text(encoding="utf-8"))
POSITION = json.loads((ROOT / "machine" / "canonical-position.json").read_text(encoding="utf-8"))
CAPABILITIES = json.loads((ROOT / "machine" / "capabilities.json").read_text(encoding="utf-8"))


class CanonicalPositionContractTests(unittest.TestCase):
    def test_evolving_state_is_gate_complete(self):
        self.assertEqual(STATE["principal_state"], "EVOLVING")
        self.assertEqual(STATE["gates"]["CANONICAL_POSITION_RESOLVED"]["status"], "PASS")
        self.assertEqual(STATE["gates"]["EVOLUTION_CURSOR_DEFINED"]["status"], "PASS")
        self.assertEqual(STATE["canonical_position_ref"], "machine/canonical-position.json")

    def test_identity_and_lineage_are_preserved(self):
        self.assertEqual(POSITION["repository"], STATE["repository"])
        self.assertEqual(POSITION["canonical_identity"], "telemetry-anomaly-receipt")
        policy = POSITION["integration_policy"]
        self.assertTrue(policy["preserve_repository_identity"])
        self.assertTrue(policy["preserve_lineage"])
        self.assertTrue(policy["absorption_requires_functional_equivalence"])
        self.assertTrue(policy["absorption_requires_proof_equivalence"])

    def test_capabilities_name_repository_native_telemetry_mechanisms(self):
        self.assertEqual(
            CAPABILITIES["capability_family"], "telemetry_anomaly_evidence_receipts"
        )
        capabilities = set(CAPABILITIES["capabilities"])
        self.assertIn("deterministic-anomaly-receipts", capabilities)
        self.assertIn("threshold-residual-evidence", capabilities)
        self.assertIn("unknown-channel-hard-anomaly", capabilities)
        self.assertIn("suppression-visible-receipt-fingerprints", capabilities)
        self.assertNotIn("hyper-scaling", capabilities)

    def test_command_edge_is_complementary_not_integrated(self):
        self.assertEqual(len(POSITION["relationships"]), 1)
        edge = POSITION["relationships"][0]
        self.assertEqual(edge["repository"], "GlacierEQ/nasa-command-authority-half-life")
        self.assertEqual(edge["integration_state"], "NOT_CLAIMED")

    def test_evolution_and_public_boundary_are_material(self):
        self.assertIn("time-series window provenance", POSITION["next_evolution"])
        self.assertIn("no NASA affiliation", POSITION["nonclaims"])
        self.assertIn("No NASA adoption", CAPABILITIES["truth_boundary"])


if __name__ == "__main__":
    unittest.main()
