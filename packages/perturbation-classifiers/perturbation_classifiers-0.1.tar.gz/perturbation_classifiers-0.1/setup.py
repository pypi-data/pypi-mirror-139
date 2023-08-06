#!/usr/bin/env python

import codecs
import os
from distutils.core import setup

from setuptools import find_packages

setup_path = os.path.abspath(os.path.dirname(__file__))
with codecs.open(os.path.join(setup_path, 'README.rst'), encoding='utf-8-sig') as f:
    README = f.read()

setup(
    name='perturbation_classifiers',
    version='0.1',
    url='https://github.com/rjos/perturbation-classifiers',
    maintainer='Rodolfo J. O. Soares',
    maintainer_email='rodolfoj.soares@gmail.com',
    description='Implementation of perturbation-based classifiers',
    long_description=README,
    long_description_content_type='text/markdown',
    author='Rodolfo J. O. Soares',
    author_email='rodolfoj.soares@gmail.com',
    license="MIT",
    
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: 3.7',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
    ],

    install_requires=[
        'scikit-learn>=0.24.2',
        'numpy>=1.21.2',
        'scipy>=1.7.1',
        'matplotlib>=3.4.3',
        'pandas>=1.3.2',
        'gap-stat>=2.0.1',
        'gapstat-rs>=2.0.1',
    ],
    python_requires='>=3.7',

    packages=find_packages()
)