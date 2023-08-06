#!/usr/bin/env python
from setuptools import setup, find_packages

__VERSION__ = '5.0.0'

setup(
    name='sanetime_py3',
    version=__VERSION__,
    author='prior',
    author_email='mprior@hubspot.com',
    maintainer='finkernagel',
    maintainer_email='finkernagel@imt.uni-marburg.de',
    packages=find_packages(),
    url='http://github.com/TyberiusPrime/sanetime',
    download_url='https://github.com/TyberiusPrime/sanetime/tarball/v%s'%__VERSION__,
    license="MIT License",
    description='A sane date/time python interface:  better epoch time, timezones, and deltas -- django support as well. Now with python3 support',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    install_requires=[
        'pytz',
        'python-dateutil',
        'unittest2'
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Topic :: Database',
        'Topic :: Internet',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP :: WSGI',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Scientific/Engineering :: Physics',
        'Topic :: Software Development',
        'Topic :: Software Development :: Internationalization',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Localization',
        'Topic :: Utilities',
    ],
    include_package_data=True,
    test_suite='sanetime.test',
    platforms=['any']
)

