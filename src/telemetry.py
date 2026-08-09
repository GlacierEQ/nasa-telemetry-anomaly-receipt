"""Telemetry anomaly receipt — deterministic threshold evidence."""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from enum import Enum


def digest(obj: object) -> str:
    return hashlib.sha256(json.dumps(obj, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


class Severity(str, Enum):
    NOMINAL = "NOMINAL"
    WARN = "WARN"
    HARD = "HARD"


@dataclass(frozen=True)
class ChannelLimit:
    channel: str
    warn: float
    hard: float


@dataclass(frozen=True)
class AnomalyReceipt:
    channel: str
    value: float
    severity: Severity
    residual: float
    suppressed: bool
    fingerprint: str


class TelemetryAnomalyMonitor:
    def __init__(self, limits: list[ChannelLimit]):
        self._limits = {l.channel: l for l in limits}
        self._acks: set[str] = set()

    def observe(self, channel: str, value: float, ack_token: str | None = None) -> AnomalyReceipt:
        lim = self._limits.get(channel)
        if lim is None:
            body = {"ch": channel, "sev": "HARD", "r": "UNKNOWN_CHANNEL"}
            return AnomalyReceipt(channel, value, Severity.HARD, 0.0, False, digest(body))
        if value >= lim.hard:
            sev = Severity.HARD
            residual = value - lim.hard
        elif value >= lim.warn:
            sev = Severity.WARN
            residual = value - lim.warn
        else:
            sev = Severity.NOMINAL
            residual = 0.0
        suppressed = False
        if sev is not Severity.NOMINAL and ack_token:
            if ack_token.startswith("ack:") and ack_token in self._acks:
                suppressed = True
        body = {
            "ch": channel,
            "v": value,
            "sev": sev.value,
            "residual": residual,
            "suppressed": suppressed,
        }
        return AnomalyReceipt(channel, value, sev, residual, suppressed, digest(body))

    def register_ack(self, token: str) -> None:
        if not token.startswith("ack:"):
            raise ValueError("BAD_ACK")
        self._acks.add(token)
