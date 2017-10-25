#!/usr/bin/env python3

# === IMPORTS ===
import logging
import os
import redpipe
import unittest

from inovonics.cloud.datastore import InoRedis

# === GLOBALS ===

# === FUNCTIONS ===

# === CLASSES ===
class TestCasesInoRedis(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        self.logger = logging.getLogger(type(self).__name__)
        super().__init__(*args, **kwargs)

    def setUp(self):
        self.redis_host = os.getenv('REDIS_HOST', 'localhost')
        self.redis_port = os.getenv('REDIS_PORT', 6379)
        self.redis_db = os.getenv('REDIS_DB', 0)

    def test_connect_to_db(self):
        # Connect to the database
        dstore = InoRedis(host=self.redis_host, port=self.redis_port, db=self.redis_db)
        # Flush the database
        dstore.redis.flushdb()
        # Write a value to a key
        dstore.redis.set('TESTKEY', 'TESTVALUE')
        # Read the value back from the key
        test_value = dstore.redis.get('TESTKEY')
        # Compare the values to make sure everything is happy
        # Flush the database
        dstore.redis.flushdb()

    def test_connect_redpipe(self):
        pass

    def tearDown(self):
        pass

# === MAIN ===
if __name__ == '__main__':
    # THIS SCRIPT SHOULD NEVER BE CALLED DIRECTLY
    # Call from the base directory of the package with the following command:
    # python3 -m unittest tests.<name_of_module>.<name_of_class>
    pass
