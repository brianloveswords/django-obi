#!/usr/bin/env python
from setuptools import setup, find_packages


setup(
    name='django-obi',
    version='0.2',
    description="Django open badge integration.",
    long_description=open('README.md', 'r').read(),
    author='Brian J Brennan; Zuzel Vera',
    url='https://github.com/brianlovesdata/django-obi',
    packages=find_packages(),
)
