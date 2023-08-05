"""A  setup module"""

from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

setup(
    name='astproject',
    version='1.0.1',
    packages=find_packages(where='hw1_package'),
    python_requires='>=3.6, <4',
)
