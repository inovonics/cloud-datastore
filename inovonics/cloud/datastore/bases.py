#!/usr/bin/env python3

# === IMPORTS ===
import logging
import redis
import redpipe
import uuid

# === GLOBALS ===

# === FUNCTIONS ===

# === CLASSES ===
class InoModelBase:
    def __init__(self, datastore):
        self.datastore = datastore  # Should be of type InoRedis or a derivative.
        self.logger = logging.getLogger(type(self).__name__)

# FIXME: Add an object base class here
class InoObjectBase:
    # Override fields to give objects attributes
    # Each field should be specified in the 'fields' list by a dictionary containing two entries: 'name' and 'type'.
    # - 'name' can be a string and will be used as the label in the database.  This should match the names/labels used 
    # in the DB* objects.
    # - 'type' should be one of the following: 'bool', 'datetime', 'int', 'str', 'uuid'
    
    # A field with name 'oid' is the object's unique identifier.  This had be named to prevents collisions with the id()
    # method.
    fields = [{'name': 'oid', 'type': 'uuid'}]
    custom_fields = [] # All custom fields are strings.
    
    allowed_types = ['bool', 'datetime', 'float', 'int', 'str', 'uuid']
    
    def __init__(self, dictionary=None):
        self.logger = logging.getLogger(type(self).__name__)
        # Setup all of the other attributes so they can be written directly
        for field in self.fields:
            if field['type'] == 'bool':
                setattr(self, field['name'], False)
            elif field['type'] == 'datetime':
                setattr(self, field['name'], datetime.datetime.utcnow())
            elif field['type'] == 'float':
                setattr(self, field['name'], 0.0)
            elif field['type'] == 'int':
                setattr(self, field['name'], 0)
            elif field['type'] == 'str':
                setattr(self, field['name'], '')
            elif field['type'] == 'uuid':
                setattr(self, field['name'], uuid.uuid4())
            else:
                raise TypeError
        if dictionary:
            self.set_fields(dictionary)

    def __repr__(self):
        return "<{}: {}>".format(type(self), self.oid)

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
        for field in self.custom_fields:
            dictionary[field] = getattr(self, field)
        return dictionary

    def set_fields(self, dictionary):
        if dictionary:
            for field in dictionary:
                if field in [i['name'] for i in self.fields]:
                    field_entry = [i for i in self.fields if i['name'] == field][0]
                    if field_entry['type'] == 'datetime':
                        setattr(self, field_entry['name'], dateutil.parser.parse(dictionary[field]))
                    elif field_entry['type'] == 'uuid':
                        setattr(self, field_entry['name'], uuid.UUID(dictionary[field]))
                    else:
                        setattr(self, field_entry['name'], dictionary[field])
                elif field in self.custom_fields:
                    setattr(self, field, dictionary[field])
                elif field.startswith('custom_'):
                    self.custom_fields.append(field)
                    setattr(self, field, dictionary[field])
        return self._validate_fields()

    def _validate_fields(self):
        # Override this function to provide field validation for the objects
        errors = []
        return errors

# === MAIN ===
