#!/usr/bin/env python
from setuptools import setup, find_packages


setup(
    name='django-obi',
    version='0.1',
    description="Django open badge integration.",
    long_description=open('README.md', 'r').read(),
    author='Brian J Brennan',
    url='https://github.com/brianlovesdata/django-obi',
    packages=find_packages(),
)
