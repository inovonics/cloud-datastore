#!/usr/bin/env python3

# === IMPORTS ===
import logging
import redis
import redpipe

# === GLOBALS ===

# === FUNCTIONS ===

# === CLASSES ===
class InoModelBase:
    def __init__(self, datastore):
        self.datastore = datastore  # Should be of type InoRedis or a derivative.
        self.logger = logging.getLogger(type(self).__name__)

# FIXME: Add an object base class here

# === MAIN ===
