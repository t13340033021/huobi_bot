#!/usr/bin/env python3
from setuptools import setup

setup(
    name="huobi-client",
    version="1.0.13",
    packages=['huobi', 'huobi.impl', 'huobi.impl.utils', 'huobi.exception', 'huobi.model', 'huobi.base', 'huobi.constant',
              "performance", "tests", "huobi.demo_service", "huobi.demo_service.mbp"],
    install_requires=['requests', 'apscheduler', 'websocket-client', 'urllib3']
)

