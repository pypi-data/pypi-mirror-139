"""A  setup module"""

from setuptools import setup
import pathlib

here = pathlib.Path(__file__).parent.resolve()

setup(
    name='astproject',
    version='1.0.2',
    package_dir={"":"src"},
    python_requires='>=3.6, <4',
)
