
# File: setup.py 
# Author(s): Vedant Sanil
# Created: Wed Feb 17 11:49:20 EST 2022 
# Description:
# Acknowledgements:
# Copyright (c) 2022 Carnegie Mellon University
# This code is subject to the license terms contained in the code repo.

import os
import sys
import shutil
import setuptools
import subprocess
from glob import glob
from distutils.command.build_py import build_py

from autonml import __VERSION__

NAME = 'autonml'
VERSION = __VERSION__

with open('basic-requirements.txt', 'r') as reqfile:
    req = [line.strip() for line in reqfile if line and not line.startswith('#')]

with open('requirements.txt', 'r') as rfile:
    breq = [line.strip() for line in rfile if line and not line.startswith('#')]

def run(args):
    subprocess.run(args, stdout=sys.stdout, stderr=sys.stdout, check=True, encoding='utf8')
    sys.stdout.flush()

# # Install packages
# options = ['--use-deprecated=legacy-resolver', '--no-cache-dir']
# basic_args = ['pip', 'install', '-r', 'basic-requirements.txt'] + options
# d3m_args = ['pip', 'install', '-r', 'requirements.txt'] + options

# # Install basic and D3M dependencies
# run(basic_args)
# run(d3m_args)

# # Install additional packages
# # TODO (vedant) : these can be removed later as the following packages are pushed to pypi
# esrnn_args = ['pip', 'install', '--index-url', 'https://test.pypi.org/simple/', '--no-deps', 'd3m-esrnn']
# nbeats_args = ['pip', 'install', '--index-url', 'https://test.pypi.org/simple/', '--no-deps', 'd3m-nbeats']
# run(esrnn_args)
# run(nbeats_args)

# print("Setup successful")

pkgs = [elem.replace('autonml/', '') for elem in glob('autonml/static/*', recursive=True) if os.path.isfile(elem)]

setuptools.setup(
    name=NAME,
    version=VERSION,
    install_requires=req,
    extras_require={
        'd3m' : breq
    },
    description=r"$AutonML$ : CMU's AutoML System",
    package_data={NAME:pkgs},
    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts': [
            'autonml_main=autonml.main:main_run',
            'automl_search=autonml.main:main_search']},
    python_requires=">=3.6",
    include_package_data=True,
    dependency_links = [ 
        'https://github.com/alkaline-ml/pmdarima/archive/refs/tags/v1.8.1.tar.gz',
        'https://github.com/uncharted-distil/distil-primitives.git@666233600447f7c4cc09fbd0e59c87ca5b842011#egg=distil-primitives',
        'https://gitlab.com/datadrivendiscovery/contrib/kungfuai-primitives.git@49acb225bb6994d3dfaffdf3b7761395423680a4#egg=kf-d3m-primitives'
    ],
    author='Saswati Ray, Andrew Williams, Vedant Sanil',
    maintainer='Andrew Williams, Vedant Sanil',
    maintainer_email='awilia2@andrew.cmu.edu, vsanil@andrew.cmu.edu',
    keywords=['datadrivendiscovery', 'automl', 'd3m', 'ta2', 'cmu'],
    license='Apache-2.0',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: Apache Software License',
        'Topic :: Scientific/Engineering']
)