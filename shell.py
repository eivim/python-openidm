#!/usr/bin/env python
import code, sys

from openidm import Client
from openidm.models import OpenIDMObject

sys.tracebacklimit = 0

openidm = client = Client(baseURL="http://localhost:8080/openidm",
    username="openidm-admin", password="openidm-admin")

banner = """Python Interactive Shell for OpenIDM Client"""
code.interact(local=locals(), banner=banner)
