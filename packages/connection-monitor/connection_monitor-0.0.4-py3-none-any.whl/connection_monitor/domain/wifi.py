"""This module provides wifi router statistics.

This is tightly coupled to NB6V router, and its login and status pages!

"""

import logging
from typing import Iterator

import requests
from bs4 import BeautifulSoup

from . import model

#: URL for login, that redirects to status page
AUTH_URL = "http://192.168.1.1/login"
#: URL for retrieving router statistics
STATUS_URL = "http://192.168.1.1/state/wan"

#: hard-coded mapping of router data, as appearing on status page
ROUTER_STATS_MAPPING = dict(
    mode=6,
    uptime=7,
    down_bandwidth=0,
    down_margin=2,
    down_attenuation=4,
    up_bandwidth=1,
    up_margin=3,
    up_attenuation=5,
)


def parse_uptime(s: str) -> str:
    return s.replace("\n", "").replace(" ", "")


def parse_field(s: str) -> str:
    return s.split("\xa0")[0]


def router_stater(secrets: model.RouterSecrets) -> Iterator[model.RouterStatistics]:
    """Generator to retrieve router statistics."""
    session = requests.Session()
    while True:
        r = session.get(url=STATUS_URL)
        # check connection
        if r.status_code == 401:
            logging.debug("authenticating to router")
            login(session, secrets)
            r = session.get(url=STATUS_URL)
        if r.status_code == 401:
            logging.warning("could not authenticate to router!")
            yield model.RouterStatistics()
        else:
            # extract statistics, here again retro-engineered from NB6V status page
            yield parse_status_page(r)


def parse_status_page(r: requests.Response) -> model.RouterStatistics:
    if r.url != STATUS_URL:
        raise ValueError(f"cannot parse router stats from {r.url}")
    stats_soup = BeautifulSoup(r.text, features="html.parser").find(id="adsl_info")
    stats = [td.text for td in stats_soup.find_all("td")]
    return model.RouterStatistics(
        mode=stats[ROUTER_STATS_MAPPING["mode"]],
        uptime=parse_uptime(stats[ROUTER_STATS_MAPPING["uptime"]]),
        down=model.Stats(
            bandwidth=parse_field(stats[ROUTER_STATS_MAPPING["down_bandwidth"]]),
            margin=parse_field(stats[ROUTER_STATS_MAPPING["down_margin"]]),
            attenuation=parse_field(stats[ROUTER_STATS_MAPPING["down_attenuation"]]),
        ),
        up=model.Stats(
            bandwidth=parse_field(stats[ROUTER_STATS_MAPPING["up_bandwidth"]]),
            margin=parse_field(stats[ROUTER_STATS_MAPPING["up_margin"]]),
            attenuation=parse_field(stats[ROUTER_STATS_MAPPING["up_attenuation"]]),
        ),
    )


def login(session: requests.Session, secrets: model.RouterSecrets) -> None:
    # authentication data -- retro-engineered from NB6V login page
    auth_data = dict(
        method="passwd",
        login=secrets.username,
        password=secrets.password,
    )
    session.post(url=AUTH_URL, data=auth_data, allow_redirects=False)
