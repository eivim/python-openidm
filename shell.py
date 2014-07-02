#!/usr/bin/env python
import code

from openidm import Client
from openidm.models import ManagedUser

c = openidm = client = Client()

banner = """Python Interactive Shell for OpenIDM Client"""
code.interact(local=locals(), banner=banner)