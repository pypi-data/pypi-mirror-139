"""User parameters for the application.

As some point, it would be better to move this in a flat file (i.e. an .ini file).

"""
from pathlib import Path
from typing import List

#: time between two requests (seconds)
DEFAULT_DELAY: float = 30.0
#: default host for latency checking
DEFAULT_HOSTS: List[str] = [
    "http://sfr.fr",
    "http://orange.com",
    "http://oui.sncf",
    "http://lemonde.fr",
    "http://ouvaton.coop/",
]
#: default timeout for latency measurement (seconds)
DEFAULT_TIMEOUT: float = 5
#: default path for writing the stats
DEFAULT_OUT_PATH: Path = Path(".")
#: default filename for writing the stats
DEFAULT_OUT_FFN: Path = DEFAULT_OUT_PATH / "network_data.csv"
#: default CSV parameters
CSV_PARAMS = dict(delimiter=";", lineterminator="\n")
