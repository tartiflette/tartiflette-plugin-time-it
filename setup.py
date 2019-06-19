import os
import subprocess
import sys

from setuptools import find_packages, setup

_TEST_REQUIRE = [
    "pytest==4.5.0",
    "pytest-cov==2.6.1",
    "pytest-asyncio==0.10.0",
    "pylint==2.3.0",
    "xenon==0.5.5",
    "black==18.9b0",
    "isort==4.3.4",
]

_VERSION = "0.0.1"

_PACKAGES = find_packages(exclude=["tests*"])


def _read_file(filename):
    with open(filename) as afile:
        return afile.read()


setup(
    name="tartiflette-plugin-time-it",
    version=_VERSION,
    description="A tartiflette plugin that will print execution duration of a field",
    long_description=_read_file("README.md"),
    long_description_content_type="text/markdown",
    url="https://github.com/tartiflette/tartiflette-plugin-time-it",
    author="Aurelien Busi",
    author_email="aurelien.busi@dailymotion.com",
    license="MIT",
    classifiers=[
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
    keywords="api graphql protocol api tartiflette",
    packages=_PACKAGES,
    install_requires=["tartiflette>=0.11.1"],
    tests_require=_TEST_REQUIRE,
    extras_require={"test": _TEST_REQUIRE},
    include_package_data=True,
)
