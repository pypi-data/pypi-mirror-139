#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path

from setuptools import find_packages, setup

# Package meta-data.
NAME = "heart disease classification model"
DESCRIPTION = "Classifying whether the patient will survive"
URL = "https://github.com/ChngYuanLongRandy/demo_deploy"
EMAIL = "chngyuanlong@gmail.com"
AUTHOR = "RandyChng"
REQUIRES_PYTHON = "==3.10.0"
VERSION = "0.0.9"


# The rest you shouldn't have to touch too much :)
# ------------------------------------------------
# Except, perhaps the License and Trove Classifiers!
# If you do change the License, remember to change the
# Trove Classifier for that!
with open("README.md", "r") as f:
    long_description = f.read()


def list_reqs(fname="requirements.txt"):
    with open(fname) as fd:
        return fd.read().splitlines()


# Where the magic happens:
setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(exclude=("tests",)),
    # package_data={"regression_model": ["VERSION"]},
    install_requires=list_reqs(),
    # extras_require={},
    include_package_data=True,
    license="BSD-3",
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
    ],
)
