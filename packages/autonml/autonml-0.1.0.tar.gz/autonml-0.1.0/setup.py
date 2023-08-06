
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

def run(args):
    subprocess.run(args, stdout=sys.stdout, stderr=sys.stdout, check=True, encoding='utf8')
    sys.stdout.flush()

# Install packages
options = ['--use-deprecated=legacy-resolver', '--no-cache-dir']
basic_args = ['pip', 'install', '-r', 'basic-requirements.txt'] + options
d3m_args = ['pip', 'install', '-r', 'requirements.txt'] + options

# Install basic and D3M dependencies
run(basic_args)
run(d3m_args)

# Install additional packages
# TODO (vedant) : these can be removed later as the following packages are pushed to pypi
esrnn_args = ['pip', 'install', '--index-url', 'https://test.pypi.org/simple/', '--no-deps', 'd3m-esrnn']
nbeats_args = ['pip', 'install', '--index-url', 'https://test.pypi.org/simple/', '--no-deps', 'd3m-nbeats']
run(esrnn_args)
run(nbeats_args)

print("Setup successful")

pkgs = [elem.replace('autonml/', '') for elem in glob('autonml/static/*', recursive=True) if os.path.isfile(elem)]

setuptools.setup(
    name=NAME,
    version=VERSION,
    #install_requires=req,
    description=r"$AutonML$ : CMU's AutoML System",
    package_data={NAME:pkgs},
    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts': [
            'autonml_main=autonml.main:main_run',
            'automl_search=autonml.main:main_search']},
    python_requires=">=3.6",
    include_package_data=True,
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