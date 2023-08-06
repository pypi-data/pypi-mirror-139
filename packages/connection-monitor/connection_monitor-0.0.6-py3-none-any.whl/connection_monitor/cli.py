from __future__ import annotations
import logging
from pathlib import Path
from typing import List

import click

from . import params, VERBOSITY
from .domain import core, model


@click.command()
@click.option(
    "-s",
    "--secrets-ffn",
    type=Path,
    default=params.DEFAULT_OUT_PATH / "secrets.yml",
    help="Filename for secrets, in YAML format.",
)
@click.option(
    "-o",
    "--out-ffn",
    type=Path,
    default=params.DEFAULT_OUT_FFN,
    help=(
        "Filename for writing measurements. This file is opened "
        "in append mode, so previous data is kept."
    ),
)
@click.option(
    "-h",
    "--hosts",
    type=str,
    multiple=True,
    default=params.DEFAULT_HOSTS,
    help="Hosts to connect to, to measure latency.",
)
@click.option(
    "-d",
    "--delay",
    type=float,
    default=params.DEFAULT_DELAY,
    help="Time (in seconds) between two measurements.",
)
@click.option(
    "-v",
    "--verbose",
    count=True,
    default=0,
    help=(
        "Increase verbosity; default is to display WARNING "
        "messages and higher. Set once, displays also INFO "
        "messages; repeated, displays also DEBUG messages."
    ),
)
@click.version_option()
def cli(
    secrets_ffn: Path,
    out_ffn: Path,
    hosts: List[str],
    delay: float,
    verbose: int,
) -> None:
    """Starts the monitoring."""
    logging.basicConfig(level=VERBOSITY[verbose])
    secrets = model.RouterSecrets.from_yaml(ffn=secrets_ffn)
    core.monitor(secrets=secrets, out_path=Path(out_ffn), hosts=hosts, delay=delay)
