from setuptools import setup, find_packages, Extension
from os import path

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='koin',
    version='0.0.2',
    description='A simple library for Coinbase Pro',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/ernestomonroy/koin',
    author='Ernesto Monroy',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3'
    ],
    keywords='meli',
    packages=find_packages(include=['koin']),
    python_requires='>=3.5',
    project_urls={
        'Bug Reports': 'https://github.com/ernestomonroy/koin/issues',
        'Source': 'https://github.com/ernestomonroy/koin',
    },
)