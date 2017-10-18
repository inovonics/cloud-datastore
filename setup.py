#!/usr/bin/env python3

# === IMPORTS ===
from setuptools import setup

# === GLOBALS ===

# === FUNCTIONS ===

# === CLASSES ===

# === MAIN ===
setup(
    name='inovonics_cloud_datastore',
    version='0.1.0.0',
    description='Basic classes for building a datastore using Redis as a backend.',
    author='Daniel Williams',
    author_email='dwilliams@inovonics.com',
    license='MIT',
    install_requires=[line.strip() for line in open('requirements.txt', 'r')],
    packages=['inovonics.cloud.datastore']
)
