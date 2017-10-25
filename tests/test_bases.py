#!/usr/bin/env python3

# === IMPORTS ===
import logging
import os
import unittest

from inovonics.cloud.datastore import InoRedis, InoModelBase

# === GLOBALS ===
logging.basicConfig(level=logging.DEBUG)

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

    def test_make_model_base(self):
        # Connect to the database
        dstore = InoRedis(host=self.redis_host, port=self.redis_port, db=self.redis_db)
        # Flush the database
        dstore.redis.flushdb()
        # Create a model base object
        model_base = InoModelBase(dstore)
        # Make sure something was created
        self.assertIsNotNone(model_base)
        # Flush the database
        dstore.redis.flushdb()
        # Force deletion of the dstore object (to force garbage collection).  This is due to an issue on the Travis-CI
        # environment of instantiating the next test before the current test is garbage collected.
        del dstore

    def tearDown(self):
        pass

# === MAIN ===
if __name__ == '__main__':
    # THIS SCRIPT SHOULD NEVER BE CALLED DIRECTLY
    # Call from the base directory of the package with the following command:
    # python3 -m unittest tests.<name_of_module>.<name_of_class>
    pass
