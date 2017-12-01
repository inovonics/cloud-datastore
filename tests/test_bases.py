#!/usr/bin/env python3

# === IMPORTS ===
import datetime
import logging
import os
import unittest
import uuid

from inovonics.cloud.datastore import InoRedis, InoModelBase, InoObjectBase

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
        del model_base
        del dstore

    def tearDown(self):
        pass

class TestCasesInoObjectBase(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        self.logger = logging.getLogger(type(self).__name__)
        super().__init__(*args, **kwargs)

    def setUp(self):
        pass

    def test_make_object_base(self):
        # Create an object base object
        object_base = InoObjectBase()
        # Make sure something was created
        self.assertIsNotNone(object_base)
        self.assertIsInstance(object_base, InoObjectBase)

    def test_make_object_base_with_bool(self):
        # Create a subclass specifying a bool field
        class TestBool(InoObjectBase):
            fields = [{'name': 'oid', 'type': 'uuid'}, {'name': 'bool1', 'type': 'bool'}]
        # Create a TestBool object
        test_bool_1 = TestBool({'bool1': False})
        # Make sure something was created
        self.assertIsNotNone(test_bool_1)
        self.assertIsInstance(test_bool_1, InoObjectBase)
        # Make sure the bool is correctly set
        self.assertFalse(test_bool_1.bool1)
        # Get the dictionary of values
        dict_test_bool_1 = test_bool_1.get_dict()
        # Make sure the bool is correctly set
        self.assertFalse(dict_test_bool_1['bool1'])

    def test_make_object_base_with_datetime(self):
        # Create a datetime that we can use throughout the test
        tmp_datetime = datetime.datetime.utcnow()
        # Create a subclass specifying a datetime field
        class TestDatetime(InoObjectBase):
            fields = [{'name': 'oid', 'type': 'uuid'}, {'name': 'datetime1', 'type': 'datetime'}]
        # Create a TestDatetime object
        test_dt_1 = TestDatetime({'datetime1': tmp_datetime.isoformat()})
        # Make sure something was created
        self.assertIsNotNone(test_dt_1)
        self.assertIsInstance(test_dt_1, InoObjectBase)
        # Make sure the datetime is correctly set
        self.assertEqual(test_dt_1.datetime1, tmp_datetime)
        # Get the dictionary of values
        dict_test_dt_1 = test_dt_1.get_dict()
        # Make sure the datetime is correctly set
        self.assertEqual(dict_test_dt_1['datetime1'], tmp_datetime.isoformat())

    def test_make_object_base_with_float(self):
        # Create a float that we can use throughout the test
        tmp_float = 0.123
        # Create a subclass specifying a float field
        class TestFloat(InoObjectBase):
            fields = [{'name': 'oid', 'type': 'uuid'}, {'name': 'float1', 'type': 'float'}]
        # Create a TestFloat object
        test_float_1 = TestFloat({'float1': tmp_float})
        # Make sure something was created
        self.assertIsNotNone(test_float_1)
        self.assertIsInstance(test_float_1, InoObjectBase)
        # Make sure the float is correctly set
        self.assertEqual(test_float_1.float1, tmp_float)
        # Get the dictionary of values
        dict_test_float_1 = test_float_1.get_dict()
        # Make sure the float is correctly set
        self.assertEqual(dict_test_float_1['float1'], tmp_float)

    def test_make_object_base_with_int(self):
        # Create a int that we can use throughout the test
        tmp_int = 147
        # Create a subclass specifying a int field
        class TestInt(InoObjectBase):
            fields = [{'name': 'oid', 'type': 'uuid'}, {'name': 'int1', 'type': 'int'}]
        # Create a TestInt object
        test_int_1 = TestInt({'int1': tmp_int})
        # Make sure something was created
        self.assertIsNotNone(test_int_1)
        self.assertIsInstance(test_int_1, InoObjectBase)
        # Make sure the int is correctly set
        self.assertEqual(test_int_1.int1, tmp_int)
        # Get the dictionary of values
        dict_test_int_1 = test_int_1.get_dict()
        # Make sure the int is correctly set
        self.assertEqual(dict_test_int_1['int1'], tmp_int)

    def test_make_object_base_with_str(self):
        # Create a string that we can use throughout the test
        tmp_str = 'Test string'
        # Create a subclass specifying a string field
        class TestStr(InoObjectBase):
            fields = [{'name': 'oid', 'type': 'uuid'}, {'name': 'str1', 'type': 'str'}]
        # Create a TestStr object
        test_str_1 = TestStr({'str1': tmp_str})
        # Make sure something was created
        self.assertIsNotNone(test_str_1)
        self.assertIsInstance(test_str_1, InoObjectBase)
        # Make sure the string is correctly set
        self.assertEqual(test_str_1.str1, tmp_str)
        # Get the dictionary of values
        dict_test_str_1 = test_str_1.get_dict()
        # Make sure the string is correctly set
        self.assertEqual(dict_test_str_1['str1'], tmp_str)

    def test_make_object_base_with_uuid(self):
        # Create a uuid that we can use throughout the test
        tmp_uuid = uuid.uuid4()
        # Create a subclass specifying a uuid field
        class TestUUID(InoObjectBase):
            fields = [{'name': 'oid', 'type': 'uuid'}, {'name': 'uuid1', 'type': 'str'}]
        # Create a TestUUID object
        test_uuid_1 = TestUUID({'uuid1': str(tmp_uuid)})
        # Make sure something was created
        self.assertIsNotNone(test_uuid_1)
        self.assertIsInstance(test_uuid_1, InoObjectBase)
        # Make sure the uuid is correctly set
        self.assertEqual(test_uuid_1.uuid1, tmp_uuid)
        # Get the dictionary of values
        dict_test_uuid_1 = test_uuid_1.get_dict()
        # Make sure the uuid is correctly set
        self.assertEqual(dict_test_uuid_1['uuid1'], str(tmp_uuid))

    def test_make_object_base_with_custom_field(self):
        # Create a string that we can use throughout the test
        tmp_custom_str = 'Custom test string'
        # Create an object base object with a custom field
        object_base = InoObjectBase({'custom_string': tmp_custom_str})
        # Make sure something was created
        self.assertIsNotNone(object_base)
        self.assertIsInstance(object_base, InoObjectBase)
        # Make sure the string is correctly set
        self.assertEqual(object_base.custom_string, tmp_custom_str)
        # Get the dictionary of values
        dict_object_base = object_base.get_dict()
        # Make sure the string is correctly set
        self.assertEqual(dict_object_base['custom_string'], tmp_custom_str)

    def tearDown(self):
        pass

# === MAIN ===
if __name__ == '__main__':
    # THIS SCRIPT SHOULD NEVER BE CALLED DIRECTLY
    # Call from the base directory of the package with the following command:
    # python3 -m unittest tests.<name_of_module>.<name_of_class>
    pass
