 # -*- coding: utf-8 -*-

"""
To upload to PyPI, PyPI test, or a local server:
python setup.py bdist_wheel upload -r <server_identifier>
"""
from setuptools import setup, find_packages

setup(
    name="ELITactive",
    version="0.2.0",
    author="Kevin M. Roccapriore",
    description="ELIT active package",
    # packages=["ELITactive", "nionswift_plugin.ELITactive"],
    packages = find_packages(),
    install_requires=["matplotlib", "numpy", "scipy","torch"],
    python_requires='~=3.6',

    keywords = ['ELIT', 'nionswift']
)