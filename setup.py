#!/usr/bin/env python

from setuptools import setup

from codecs import open
from os import path
from wagtailstreamforms import __version__

tests_require = [
    "mock==4.0.2",
    # Linting
    "isort[pyproject]==4.3.21",
    "flake8==3.7.9",
    "flake8-blind-except==0.1.1",
    "flake8-debugger==3.1.0"
]


install_requires = [
    'wagtail>=2,<2.11'
]

documentation_extras = [
    'sphinxcontrib-spelling>=2.3.0',
    'Sphinx>=1.5.2',
    'sphinx-autobuild>=0.6.0',
    'karma_sphinx_theme>=0.0.6',
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
        'docs': documentation_extras,
        'test': tests_require,
    },
    include_package_data=True,
    keywords=['wagtail', 'streamfield', 'forms', 'accent', 'design'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Framework :: Wagtail',
        'Framework :: Wagtail :: 2',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Framework :: Django',
        'Framework :: Django :: 2.0',
        'Framework :: Django :: 3.0',
        'Framework :: Wagtail',
        'Framework :: Wagtail :: 2',
        'Topic :: Internet :: WWW/HTTP :: Site Management',
    ],
)
