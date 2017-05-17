#!/usr/bin/env python3

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

import markdown
from codecs import open
from os import path

def readme():
    here = path.abspath(path.dirname(__file__))

    with open(path.join(here, 'README.md'), encoding='utf-8') as f:
        return markdown.markdown(f.read())

config = {
    'description': '''A regex solution to simplify searching for specific
    strings and offer the ability to have those masked (intended for log files
     to maintain Policy compliance).''',
    'long_description': readme(),
    'author': ['Nahum Smith', 'Shan Grant'],
    'url': 'https://github.com/nahum-smith/mom-sanitizer',
    'download_url': 'Where to download it.',
    'author_email': [
        'nahumsmith(REMOVEME)(AT)gmail(DOT)com',
        'grantpka(REMOVEME)(AT)gmail(DOT)com'
        ],
    'version': '1.0.0.dev1',
    'install_requires': ['nose', 'markdown'],
    'setup_requires': 'markdown',
    'classifiers': [
        'Operating System :: POSIX :: Linux :: Only'
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3 :: Only',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'Intended Audience :: System Auditors',
        'Topic :: System :: Logging',
        'Topic :: Security',
        'Topic :: Security :: Obfuscation',
        'Topic :: Security :: Policy Compliance',
        'Topic :: Security :: NIST :: Special Publication 800-122',
        'Topic :: System :: Directory :: Searching'
    ],
    'packages': ['mom_sanitizer'],
    'scripts': ['bin/sanitize'],
    'name': 'M.O.M. Sanitizer'
}

setup(**config)
