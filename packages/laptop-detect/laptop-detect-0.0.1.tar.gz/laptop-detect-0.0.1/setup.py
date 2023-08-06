#!/usr/bin/env python3

from setuptools import setup

setup(
    name='laptop-detect',
    version='0.0.1',
    description='A port of the popular laptop-detect shell script',
    long_description='Check out the README on [GitLab](https://gitlab.com/thomasjlsn/laptop-detect-py)!',
    long_description_content_type='text/markdown',
    author='Thomas Ellison',
    author_email='thomasjlsn@gmail.com',
    url='https://gitlab.com/thomasjlsn/laptop-detect-py',
    packages=['laptop_detect'],
    license_files=['LICENSE'],
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
    ]
)
