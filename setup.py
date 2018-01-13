import unittest

from setuptools import setup, find_packages
from codecs import open
from os import path

def custom_test_suite():
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('test', pattern='test_*.py')
    return test_suite

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'description.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name             = 'org-reports',
    version          = '0.1.1',
    description      = 'Reporting on your org-mode life',
    long_description = long_description,
    url              = 'https://github.com/pypa/org-reports',
    author           = 'Michael',
    author_email     = 'sp1ff@pobox.com',
    license          = 'GPL',
    # Cf. https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers      = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: End Users/Desktop',
        'Topic :: Software Development :: Python Modules',
        'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',
        'Programming Language :: Python :: 2.7',
    ],
    keywords         = 'emacs org org-mode todo productivity',

    # You can just specify the packages manually here if your project
    # is simple. Or you can use find_packages().
    packages = find_packages(exclude=['contrib', 'docs', 'test*']),

    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires = ['click', 'jinja2'],


    # If there are data files included in your packages that need to be
    # installed, specify them here.  If using Python 2.6 or less, then these
    # have to be included in MANIFEST.in as well.
    package_data = {
        'description': ['description.rst'],
    },

    # To provide executable scripts, use entry points in preference
    # to the"scripts" keyword. Entry points provide cross-platform
    # support and allow pip to create the appropriate form of
    # executable for the target platform.
    entry_points = {
        'console_scripts': [
            'org-reports=orgreports.main:cli',
        ],
    },
    test_suite = 'setup.custom_test_suite'
)
