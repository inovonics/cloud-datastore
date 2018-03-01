#!/usr/bin/env python3

# === IMPORTS ===
import datetime
import logging
#import redis
#import redpipe
import uuid
import sys
import re

import dateutil.parser

from inovonics.cloud.datastore import InvalidDataException

# === GLOBALS ===

# === FUNCTIONS ===

# === CLASSES ===
class InoModelBase:
    # pylint: disable=too-few-public-methods
    def __init__(self, datastore):
        self.datastore = datastore  # Should be of type InoRedis or a derivative.
        self.logger = logging.getLogger(type(self).__name__)

class InoObjectBase:
    # Override fields to give objects attributes
    # Each field should be specified in the 'fields' list by a dictionary containing two entries: 'name' and 'type'.
    # - 'name' can be a string and will be used as the label in the database.  This should match the names/labels used
    # in the DB* objects.
    # - 'type' should be one of the following: 'bool', 'datetime', 'int', 'str', 'uuid'

    # A field with name 'oid' is the object's unique identifier.  This had be named to prevents collisions with the id()
    # method.
    fields = [{'name': 'oid', 'type': 'uuid'}]

    allowed_types = ['bool', 'datetime', 'float', 'int', 'list', 'str', 'uuid']

    def __init__(self, dictionary=None):
        self.logger = logging.getLogger(type(self).__name__)
        # Setup all of the attributes so they can be written directly
        for field in self.fields:
            if field['type'] == 'bool':
                setattr(self, field['name'], False)
            elif field['type'] == 'datetime':
                setattr(self, field['name'], datetime.datetime.utcnow())
            elif field['type'] == 'float':
                setattr(self, field['name'], 0.0)
            elif field['type'] == 'int':
                setattr(self, field['name'], 0)
            elif field['type'] == 'list':
                setattr(self, field['name'], [])
            elif field['type'] == 'str':
                setattr(self, field['name'], '')
            elif field['type'] == 'uuid':
                setattr(self, field['name'], uuid.uuid4())
            else:
                raise TypeError
        # Setup the base validation methods.  Any validation methods should be added here.
        self.validation_methods = [self._validate_oid, self._validate_custom]
        # Setup the custom fields list
        self.fields_custom = []
        # If a dictionary was passed in, pass it to set_fields
        if dictionary:
            self.set_fields(dictionary)

    def __repr__(self):
        return "<{}: {}>".format(type(self), getattr(self, 'oid'))

    def get_dict(self):
        # Get all fields in the object as a dict (excluding hidden fields)
        dictionary = {}
        for field in self.fields:
            if field['type'] == 'datetime':
                dictionary[field['name']] = getattr(self, field['name']).isoformat()
            elif field['type'] == 'uuid':
                dictionary[field['name']] = str(getattr(self, field['name']))
            else:
                dictionary[field['name']] = getattr(self, field['name'])
        for field in self.fields_custom:
            dictionary[field] = getattr(self, field)
        return dictionary

    def set_fields(self, dictionary):
        if dictionary:
            for field in dictionary:
                self.logger.debug("field: %s", field)
                if field in [i['name'] for i in self.fields]:
                    field_entry = [i for i in self.fields if i['name'] == field][0]
                    self.logger.debug("field_entry: %s", field_entry)
                    if field_entry['type'] == 'datetime':
                        setattr(self, field_entry['name'], dateutil.parser.parse(dictionary[field]))
                    elif field_entry['type'] == 'uuid':
                        setattr(self, field_entry['name'], uuid.UUID(dictionary[field]))
                    else:
                        setattr(self, field_entry['name'], dictionary[field])
                elif field in self.fields_custom:
                    setattr(self, field, dictionary[field])
                elif field.startswith('custom_'):
                    self.fields_custom.append(field)
                    setattr(self, field, dictionary[field])
        return self._validate_fields()

    def _validate_fields(self):
        # This calls each of the methods listed in the validation_methods list.  Each listed method should check a value
        # and return a validation error.  If an error (not None) is returned, it's added to the list of errors, which is
        # returned from this function.
        errors = []
        self.logger.debug("self.validation_methods: %s", self.validation_methods)
        for v_method in self.validation_methods:
            error = v_method()
            if error is not None:
                errors.append(error)
        self.logger.debug("errors: %s", errors)
        if errors:
            raise InvalidDataException("Validation Error List: {}".format(errors))

    def _validate_oid(self):
        # Verify the oid is a UUID type variable
        if not isinstance(getattr(self, 'oid'), uuid.UUID):
            return "oid not of type uuid.UUID but type {}, value {}".format(
                type(getattr(self, 'oid')), getattr(self, 'oid'))
        return None

    def _validate_custom(self):
        # Verify the custom fields are type string
        for field in self.fields_custom:
            if not isinstance(getattr(self, field), str):
                return "{} not of type str but type {}, value {}".format(
                    field, type(getattr(self, field)), getattr(self, field))
            if len(getattr(self, field)) > 4096:
                return "Length of field {} greater than 4096.".format(field)
        return None

    def _validate_str(self, field_name, min=0, max=4096, required=True):
        # String >= min chars and <= max chars

        attr = getattr(self, field_name)
        # Check for empty
        if attr is None and not required:
            return None

        # Check if it is a string
        if not isinstance(attr, str):
            return "{} not of type str but type {}, value {}".format(field_name, type(attr), attr)

        # Recheck if it is empty string
        if len(attr) == 0 and not required:
            return None

        # Check for permissible lenght if attribute is present
        if len(attr) < min or len(attr) > max:
            return "{} must be between {} and {} chars".format(field_name, min, max)
        return None

    def _validate_email(self, field_name, max=4096, required=True):

        attr = getattr(self, field_name)
        if attr is None and not required:
            return None

        # Check if it is a string
        str_check = self._validate_str(field_name, 0, max, required)
        if str_check is not None:
            return str_check

        # Recheck if it is emtpy and not required
        if len(attr) == 0 and not required:
            return None

        # Check for the format
        if re.match('^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$', attr) is None:
            return "{} must be a valid email".format(field_name)

        return None

    def _validate_int(self, field_name, min=-sys.maxsize-1, max=sys.maxsize, required=True):

        attr = getattr(self, field_name)
        if attr is None and not required:
            return None

        # Do an int check
        if not isinstance(attr, int):
            return "{} not of type int but type {}, value {}".format(
                field_name, type(attr), attr)

        # Finally, do a range check
        if attr < min or attr > max:
            return "{} must be between {} and {}".format(field_name, min, max)
        return None

    def _validate_float(self, field_name, min=-sys.float_info.max, max=sys.float_info.max, required=True):

        attr = getattr(self, field_name)
        if attr is None and not required:
            return None

        # Do an float check
        if not isinstance(attr, float):
            return "{} not of type float but type {}, value {}".format(
                field_name, type(attr), attr)

        # Finally, do a range check
        if attr < min or attr > max:
            return "{} must be between {} and {}".format(field_name, min, max)
        return None

    def _validate_datetime(self, field_name, required=True):

        attr = getattr(self, field_name)
        if attr is None and not required:
            return None

        # Do a datetime check
        if not isinstance(attr, datetime.datetime):
            return "{} not of type datetime but type {}, value {}".format(
                field_name, type(attr), attr)

        return None

    def _validate_bool(self, field_name, required=True):

        attr = getattr(self, field_name)
        if attr is None and not required:
            return None

        # Type check
        if not isinstance(attr, bool):
            return "{} not of type bool but type {}, value {}".format(
                field_name, type(attr), attr)
        return None

    def _validate_list(self, field_name, min=1, required=True):

        attr = getattr(self, field_name)
        if attr is None and not required:
            return None

        # Ensure field_name is present and a list
        if not isinstance(attr, list):
            return "{} not of type list but type {}, value {}".format(
                field_name, type(attr), attr)

        # Recheck for empty when not required
        if len(attr) == 0 and not required:
            return None

        # Finally check for min length
        if len(attr) < min:
            return "{} should have at least {} elements".format(field_name, min)
        return None

    def _validate_phone(self, field_name, required=True):

        attr = getattr(self, field_name)
        if attr is None and not required:
            return None

        # Check if it is a string
        str_check=self._validate_str(field_name, min=0, max=30, required=required)

        if str_check is not None:
            return str_check

        # Check for the length
        if len(attr) == 0 and not required:
            return None

        # Check the regex....
        val = re.match('[0123456789.()#*wp \-+]*', attr)
        if  val is None or val.start() != 0 or val.end() != len(attr):
            return "{} has illegal chars, value {}".format(field_name, attr)

        return None

    def _validate_uuid(self, field_name, required=True):

        attr = getattr(self, field_name)
        if attr is None and not required:
            return None

        if not isinstance(attr, uuid.UUID):
            return "{} not of type uuid but type {}, value {}".format(
                field_name, type(attr), attr)
# === MAIN ===
