#!/usr/bin/env python

from setuptools import setup

from codecs import open
from os import path
from wagtailstreamforms import __version__


install_requires = [
    'Django>=1.11,<1.12',
    'django-model-utils>=3.0.0',
    'django-recaptcha>=1.3.1',
    'wagtail>=1.12,<2'
]

documentation_extras = [
    'sphinxcontrib-spelling>=2.3.0',
    'Sphinx>=1.5.2',
    'sphinx-autobuild>=0.6.0',
    'sphinx_rtd_theme>=0.1.9',
]

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='wagtailstreamforms',
    version=__version__,
    description='Wagtail forms in a streamfield',
    long_description=long_description,
    author='Stuart George',
    author_email='stuart@accentdesign.co.uk',
    url='https://github.com/AccentDesign/wagtailstreamforms/',
    download_url='https://pypi.python.org/pypi/wagtailstreamforms',
    license='MIT',
    packages=[
        'wagtailstreamforms'
    ],
    install_requires=install_requires,
    extras_require={
        'docs': documentation_extras
    },
    include_package_data=True,
    keywords=['wagtail', 'streamfield', 'forms', 'accent', 'design'],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
