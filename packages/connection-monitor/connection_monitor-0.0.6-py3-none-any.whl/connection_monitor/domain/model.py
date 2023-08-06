from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional

import yaml

from ..utils import convert_to_mbit


@dataclass
class Stats:
    bandwidth: str = "--"
    margin: str = "--"
    attenuation: str = "--"

    @staticmethod
    def fields() -> List[str]:
        return ["bandwidth (Kbps)", "margin (dB)", "attenuation (dB)"]

    def values(self) -> List[str]:
        return [self.bandwidth, self.margin, self.attenuation]


@dataclass
class RouterStatistics:
    mode: str = "--"
    uptime: str = "--"
    down: Stats = field(default_factory=Stats)
    up: Stats = field(default_factory=Stats)

    @staticmethod
    def fields() -> List[str]:
        return (
            ["mode", "uptime"]
            + ["down " + field for field in Stats.fields()]
            + ["up " + field for field in Stats.fields()]
        )

    def values(self) -> List[str]:
        return [self.mode, self.uptime] + self.down.values() + self.up.values()


@dataclass
class NetworkStats:
    """Class to handle the network statistics.

    Addition and substraction are supported; latency is however neither
    added (righthand latency is kept) nor substracted (lefthand latency is
    kept).

    >>> ns0 = NetworkStats(bytes_in=2.2, bytes_out=3.2, latency_ms=10.2)
    >>> ns1 = NetworkStats(bytes_in=2.3, bytes_out=4.3, latency_ms=32.1)
    >>> diff = ns1 + ns0; (diff.bytes_in, diff.bytes_out, diff.latency_ms)
    (4.5, 7.5, 10.2)
    >>> diff = ns1 - ns0; (diff.bytes_in <= 0.1, diff.latency_ms == 32.1)
    (True, True)

    """

    bytes_in: float = 0.0  #: bytes
    bytes_out: float = 0.0  #: bytes
    latency_ms: float = 0.0  #: milliseconds
    router_stats: Optional[RouterStatistics] = None

    @staticmethod
    def fields() -> List[str]:
        return ["bytes_in (MB)", "bytes_out (MB)", "latency (ms)"]

    def values(self) -> List[str]:
        return [
            "{:.3f}".format(convert_to_mbit(self.bytes_in)),
            "{:.3f}".format(convert_to_mbit(self.bytes_out)),
            "{:.1f}".format(self.latency_ms),
        ]

    def __add__(self, other: NetworkStats) -> NetworkStats:
        return NetworkStats(
            bytes_in=self.bytes_in + other.bytes_in,
            bytes_out=self.bytes_out + other.bytes_out,
            latency_ms=other.latency_ms,
            router_stats=other.router_stats,
        )

    def __sub__(self, other: NetworkStats) -> NetworkStats:
        return NetworkStats(
            bytes_in=self.bytes_in - other.bytes_in,
            bytes_out=self.bytes_out - other.bytes_out,
            latency_ms=self.latency_ms,
            router_stats=self.router_stats,
        )


@dataclass
class RouterSecrets:
    username: str
    password: str

    @classmethod
    def from_yaml(cls, ffn: Path) -> RouterSecrets:
        with ffn.open(encoding="utf-8") as fh_in:
            secrets = yaml.safe_load(fh_in.read())
        return RouterSecrets(
            username=secrets["router"]["username"],
            password=secrets["router"]["password"],
        )
