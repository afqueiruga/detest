import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "detest",
    version = "0.1",
    author = "Alejandro Francisco Queiruga",
    description = "A differential equation testing suite",
    url="https://github.com/afqueiruga/detest",
    license = "GNU LGPL",
    keywords = "",
    packages = find_packages(exclude=['test']),
    test_suite='test',
    long_description=read('Readme.md'),
    long_description_content_type='text/markdown',
    classifiers=[],
)
