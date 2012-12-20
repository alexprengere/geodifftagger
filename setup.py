#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Main installation file for diff tagger.
'''

from setuptools import setup

setup(
    name = 'GeoDiffTagger',
    version = '0.1',
    author = 'Alex Prengere',
    author_email = 'alex.prengere@amadeus.com',
    description = 'Tag diff between geographical files.',
    # Manage standalone scripts
    entry_points = {
        'console_scripts' : [
            'tag_diff = tag_diff:main'
        ]
    },
    py_modules = [
        'tag_diff'
    ]
)

