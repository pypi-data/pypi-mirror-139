#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['boto3>=1.21.3', 'requests-oauthlib>=1.3.1', ]

test_requirements = ['pytest>=3', ]

setup(
    author="Jakub Boukal",
    author_email='www.bagr@gmail.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Python client for CardMarket API v3+",
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='cardmarket_api',
    name='cardmarket-api',
    packages=find_packages(include=['cardmarket_api', 'cardmarket_api.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/SukiCZ/cardmarket_api',
    version='0.1.0',
    zip_safe=False,
)
