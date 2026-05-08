#!/usr/bin/env python3
"""
Setup script for Nova CLI AI Agent
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="nova-cli",
    version="1.0.0",
    author="brextag",
    description="Nova - An intelligent CLI AI Agent",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/brextag/CODE_CLI",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "nova=nova_cli:main",
        ],
    },
    include_package_data=True,
)
