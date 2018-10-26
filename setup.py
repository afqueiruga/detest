import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "HydrogeologyTesting",
    version = "0.0.1",
    author = "Alejandro Francisco Queiruga",
    description = "",
    license = "none",
    keywords = "",
    packages=['HydrogeologyTesting'],
    test_suite='test',
    long_description=read('Readme.md'),
    classifiers=[],
)
