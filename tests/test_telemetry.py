from __future__ import annotations
import unittest
from src.telemetry import ChannelLimit, Severity, TelemetryAnomalyMonitor

class TlmTests(unittest.TestCase):
    def test_hard(self):
        m = TelemetryAnomalyMonitor([ChannelLimit("temp", 50.0, 80.0)])
        r = m.observe("temp", 90.0)
        self.assertEqual(r.severity, Severity.HARD)
        self.assertFalse(r.suppressed)

    def test_ack_suppress(self):
        m = TelemetryAnomalyMonitor([ChannelLimit("temp", 50.0, 80.0)])
        m.register_ack("ack:ops1")
        r = m.observe("temp", 60.0, ack_token="ack:ops1")
        self.assertEqual(r.severity, Severity.WARN)
        self.assertTrue(r.suppressed)

if __name__ == "__main__":
    unittest.main()
