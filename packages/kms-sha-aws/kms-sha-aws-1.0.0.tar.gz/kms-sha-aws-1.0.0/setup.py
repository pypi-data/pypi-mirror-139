from setuptools import setup, find_packages

# To use a consistent encoding
from codecs import open
from os import path

# The directory containing this file
HERE = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# This call to setup() does all the work
setup(
    name="kms-sha-aws",
    version="1.0.0",
    description="kms and hashing library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Nitish Chandna",
    license="MIT",
    packages=["kmsshademo"],
    include_package_data=True
)