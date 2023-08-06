#!/usr/bin/env python

from setuptools import find_packages, setup

install_requires = [
    'agate>=1.5.0',
]

with open('README.rst') as f:
    long_description = f.read()

setup(
    name='agate-mdb',
    version='0.0.3',
    description='agate-mdb adds read support for Microsoft Access files to agate.',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    author='Loïc Corbasson',
    author_email='loic.corbasson@gmail.com',
    url='http://agate-mdb.readthedocs.org/',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    packages=find_packages(exclude=['tests', 'tests.*']),
    install_requires=[
        'agate>=1.5.0',
     ],
    extras_require={
        'test': [
            'nose>=1.1.2',
        ],
        'docs': [
            'Sphinx>=1.2.2',
            'sphinx_rtd_theme>=0.1.6',
        ],
    }
)
