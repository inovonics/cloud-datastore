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
        self.logger.debug("test_value: %s, type: %s", test_value, type(test_value))
        self.assertEqual(test_value, 'TESTVALUE')
        # Flush the database
        dstore.redis.flushdb()

    def test_connect_redpipe(self):
        # Connect to the database
        dstore = InoRedis(host=self.redis_host, port=self.redis_port, db=self.redis_db)
        # Flush the database
        dstore.redis.flushdb()
        # Add an item with a redpipe pipeline
        with redpipe.autoexec() as pipe:
            pipe.set('TESTKEY2', 'TESTVALUE2')
        # Get the item with without a pipeline
        test_value2 = None
        with redpipe.autoexec() as pipe:
            test_value2 = pipe.get('TESTKEY2')
        # Compare the values to make sure everything is happy
        self.logger.debug("test_value2: %s, type: %s", test_value2, type(test_value2))
        self.assertEqual(test_value2, 'TESTVALUE2')
        # Flush the database
        dstore.redis.flushdb()

    def tearDown(self):
        pass

# === MAIN ===
if __name__ == '__main__':
    # THIS SCRIPT SHOULD NEVER BE CALLED DIRECTLY
    # Call from the base directory of the package with the following command:
    # python3 -m unittest tests.<name_of_module>.<name_of_class>
    pass
