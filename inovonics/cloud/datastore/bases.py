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
    # Override fields and hidden_fields to give objects attributes
    fields = []
    hidden_fields = []
    custom_fields = []
    
    def __init__(self, dictionary=None):
        self.id = str(uuid.uuid4())
        # Setup all of the attributes so they can be written directly
        for field in self.fields + self.hidden_fields:
            setattr(self, field, '')
        if dictionary:
            self.set_fields(dictionary)

    def __repr__(self):
        return "<{}: {}>".format(type(self), self.id)

    def get_dict(self):
        # Get all fields in the object as a dict (excluding hidden fields)
        dictionary = {}
        for field in self.fields + self.custom_fields:
            dictionary[field] = getattr(self, field)
        return dictionary

    def get_all_dict(self):
        # Get all fields in the object as a dict
        dictionary = {}
        for field in self.fields + self.custom_fields + self.hidden_fields:
            dictionary[field] = getattr(self, field)
        return dictionary

    def set_fields(self, dictionary):
        if not dictionary:
            return self._validate_fields()
        for field in dictionary:
            if field in self.fields + self.custom_fields + self.hidden_fields:
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
