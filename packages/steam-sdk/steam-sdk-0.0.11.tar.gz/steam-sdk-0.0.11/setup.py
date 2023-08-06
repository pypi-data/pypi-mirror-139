from setuptools import setup
from setuptools import find_packages
import pkg_resources

with open("Readme.md", "r") as fh:
    long_description = fh.read()
pkg_resources.declare_namespace(__name__)

setup(
    name='steam-sdk',
    version="0.0.11",
    author="STEAM Team",
    author_email="steam-team@cern.ch",
    description="Source code for APIs for STEAM tools.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://gitlab.cern.ch/steam/steam_sdk",
    keywords={'STEAM', 'API', 'SDK', 'CERN'},
    include_package_data=True,
    python_requires='>=3.8',
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.8"],

)
