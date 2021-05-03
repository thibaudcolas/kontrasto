#!/usr/bin/env python

import io

from setuptools import find_packages, setup  # type: ignore

from kontrasto import (
    __author__,
    __author_email__,
    __copyright__,
    __description__,
    __license__,
    __name__,
    __url__,
    __version__,
)

with io.open("README.md", encoding="utf-8") as readme_file:
    long_description = readme_file.read()

setup(
    name=__name__,
    version=__version__,
    description=__description__,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=__url__,
    author=__author__,
    author_email=__author_email__,
    license=__license__,
    copyright=__copyright__,
    packages=find_packages(exclude=["tests*"]),
    include_package_data=True,
    package_data={"kontrasto": ["py.typed"]},
    keywords=[
        "kontrasto",
        "color",
        "colour",
        "contrast",
        "dominant colors",
        "accessibility",
        "a11y",
        "wcag",
        "apca",
    ],
    python_requires=">=3.6",
    install_requires=["numpy", "Pillow"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Typing :: Typed",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    entry_points={"console_scripts": ["kontrasto=kontrasto.cli:main"]},
)
