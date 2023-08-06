#!/usr/bin/env python

from setuptools import setup

setup(
    name='pterrafile',
    version='0.5.0',
    description='Manage external Terraform modules.',
    author='Riccardo Scartozzi - Raymond Butcher',
    #author_email='',
    url='https://github.com/terraform-great-modules/python-terrafile',
    license='MIT License',
    packages=(
        'pterrafile',
    ),
    scripts=(
        'bin/pterrafile',
    ),
    install_requires=(
        'pyyaml',
        'requests',
    ),
)
