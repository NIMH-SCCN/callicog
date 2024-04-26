"""
See README.md for install instructions. This file does not enable conventional
installation via e.g. `pip install callicog`, due to dependency idiosyncracies.

This `setup.py` is used to provide conventional package metadata as well as
provide the `callicog` CLI entry point and specify `src` as package directory.


Regarding Python version, We are constrained by wxPython/PsychoPy to 3.8-3.9,
but since dependency conflicts have proved so hairy, using version 3.8.19 is
recommended, as it is known to be working.
"""
from setuptools import setup


setup(
    name="callicog",
    version="0.1.0",
    description="CalliCog. Modular touchscreen operant chamber system.",
    author="NIMH SCCN",
    author_email="brian.stewart@nih.gov",
    packages=["callicog"],
    package_dir={"": "src"},
    python_requires="~=3.8",
    # python_requires=">=3.8, <3.10",
    entry_points={
        "console_scripts": [
            "callicog=callicog.cli:callicog",
        ],
    },
	# Install requires is omitted,
    install_requires=[],
)
