#!/usr/bin/env python3

# === IMPORTS ===
import logging
import redis
import redpipe

# === GLOBALS ===

# === FUNCTIONS ===

# === CLASSES ===
class InoRedis:
    def __init__(self, host, port=6379, db=0):
        self.logger = logging.getLogger(type(self).__name__)
        self.logger.info("Initiallizing Redis and Redpipe connections.")
        # Initialize redis connection
        self.host = host
        self.port = port
        self.db = db
        self.redis = redis.StrictRedis(host=self.host, port=self.port, db=self.db)
        # Initialize redpipe connection
        redpipe.connect_redis(self.redis)

    def __del__(self):
        self.logger.info("Destructing Redis and Redpipe connections.")
        redpipe.reset()

# === MAIN ===
