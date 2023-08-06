# coding: utf-8
"""This package provides :py:func:`monitor` to build network stats.

There's also a command-line utility, installed with the package, named
``monitor``.

"""

# ---- build-in imports ---------------------------------------------------
from __future__ import annotations

import logging
import pkgutil

# ---- third-party imports ------------------------------------------------

# ---- local imports ------------------------------------------------------
from . import params

# ---- package metadata ---------------------------------------------------
#: filename providing the package version
VERSION_FN = "VERSION"
try:
    # pkgutil.get_data output is a byte stream, that needs decoding
    RAW_VERSION = pkgutil.get_data(__name__, VERSION_FN)
except FileNotFoundError:
    logging.error("Cannot retrieve version: %s", exc_info=True)
    RAW_VERSION = None

if RAW_VERSION is None:
    #: version of the package
    __version__ = "0.0.0"
else:
    __version__ = RAW_VERSION.decode()
    # sanitize string by removing blank characters
    for char in " \r\n\t":
        __version__ = __version__.replace(char, "")

# ---- constants definition -----------------------------------------------
#: verbosity levels
VERBOSITY = {0: logging.WARNING, 1: logging.INFO, 2: logging.DEBUG}
