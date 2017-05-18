#!/usr/bin/env python3

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

try:
    import markdown
    md = True
except ModuleNotFoundError:
    md = False

from codecs import open
from os import path

description = '''An expression search solution to assist with identifying
sensitive strings and offer the ability to have those masked (initially created
for log files sanitization to maintain various compliance requirements).'''

def readme(markdown_bool):
    here = path.abspath(path.dirname(__file__))

    with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
        if md:
            return markdown.markdown(f.read())
        else:
            return description

config = {
    'description': description,
    'long_description': readme(md),
    'author': ['Nahum Smith', 'Shan Grant'],
    'url': 'https://github.com/nahum-smith/mom-sanitizer',
    'download_url': 'https://github.com/nahum-smith/mom-sanitizer',
    'author_email': [
        'nahumsmithREMOVEME(AT)gmail(DOT)com',
        'shangrantREMOVEME(AT)gmail(DOT)com'
        ],
    'version': '1.0.0.dev1',
    'install_requires': ['nose', 'markdown'],
    'setup_requires': 'markdown',
    'classifiers': [
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3 :: Only',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'Topic :: Security'
    ],
    'packages': ['mom_sanitizer'],
    'scripts': ['bin/sanitize'],
    'name': 'MOM_Sanitizer'
}

setup(**config)
