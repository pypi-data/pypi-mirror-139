from __future__ import annotations

import csv
import datetime
import logging
import random
import time
from pathlib import Path
from typing import Iterator, List, Tuple

import psutil
import requests

from . import model, wifi
from .. import params


def monitor(
    secrets: model.RouterSecrets,
    out_path: Path = params.DEFAULT_OUT_PATH,
    hosts: List[str] = None,
    delay: float = params.DEFAULT_DELAY,
    csv_params: dict = None,
) -> None:
    """Monitor the network and write the stats to *out_ffn* in csv format.

    This is a wrapper around :py:func:`get_stats_in_period`, to write results
    in a file.

    Args:
        secrets: authentication data for stats retrieval
        out_path: where to write the measurements.
        hosts: list of addresses to connect for latency measurement.
        delay: time between two measurements.
        csv_params: definition of csv structure.

    """
    hosts = hosts or params.DEFAULT_HOSTS
    csv_params = csv_params or params.CSV_PARAMS
    with out_path.open("a") as fh_out:
        csv_out = csv.writer(fh_out, **csv_params)
        if fh_out.tell() == 0:  # write header only at file creation
            header = ["timestamp"]
            header.extend(model.NetworkStats.fields())
            header.append("host")
            header.extend(model.RouterStatistics.fields())
            csv_out.writerow(header)
        # TODO: the stats shall be gathered from a queue
        for (host, stats) in get_stats_in_period(secrets=secrets, hosts=hosts):
            router_stats = stats.router_stats or model.RouterStatistics()
            stats_row: List[str] = [str(datetime.datetime.now())]
            stats_row.extend(stats.values())
            stats_row.append(host)
            stats_row.extend(router_stats.values())
            csv_out.writerow(stats_row)
            logging.info("%s: in: %sMB, out: %sMB, ping: %sms to %s", *stats_row[:5])
            time.sleep(delay)
            fh_out.flush()


def get_stats_in_period(
    secrets: model.RouterSecrets,
    hosts: List[str] = None,
) -> Iterator[Tuple[str, model.NetworkStats]]:
    """Yield stats for the period between two calls.

    Args:
        secrets: authentication data for stats retrieval
        hosts: list of addresses to connect to for latency measurement.

    Yields:
        latest i/o bytes counts and latency measurement.

    """
    hosts = hosts or params.DEFAULT_HOSTS
    old_stats = model.NetworkStats()
    router_stater = wifi.router_stater(secrets)
    next(router_stater)  # init
    while True:
        # TODO: do this asynchronously, as `latency() call` is very likely to
        #  take some *seconds* when things go rough. Return value shall be
        #  pushed in a queue with the request start timestamp.
        host = random.choice(hosts)
        new_stats = model.NetworkStats(
            bytes_in=psutil.net_io_counters().bytes_recv,
            bytes_out=psutil.net_io_counters().bytes_sent,
            latency_ms=latency(host=host),
            router_stats=next(router_stater),
        )
        if old_stats.bytes_in:
            yield host, new_stats - old_stats
        old_stats = new_stats


def latency(
    host: str,
    timeout: float = params.DEFAULT_TIMEOUT,
) -> float:
    """Ping *host* and return the latency value in ms."""
    try:
        duration_ms = (
            1000.0
            * requests.head(
                host, timeout=timeout, allow_redirects=False
            ).elapsed.total_seconds()
        )
    except (requests.ConnectionError, requests.exceptions.ReadTimeout):
        duration_ms = -1.0
    return duration_ms
